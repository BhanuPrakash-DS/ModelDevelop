import os
import re
import sys
import pickle
import math
import pdb
import logging
import requests

import Discovery.ml_models.news_topic_model as tm
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
#from html.parser import HTMLParser
from HTMLParser import HTMLParser
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

#import ModelDevelop.ml_models.news_topic_model as tm
# import TopicModel

class MLStripper(HTMLParser):
    def __init__(self):
        #super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


# def strip_tags(html):
#     s = MLStripper()
#     s.feed(html)
#     return s.get_data()


def main():
    # logging.basicConfig(level=logging.DEBUG)
    # logging.debug('Begin')

    spark = SparkSession.builder.appName("Sample Process News").getOrCreate()

    ## Set URL if results have to be pushed to Elastic Search

    #     main.url = "http://idf-es.dev.spratingsvpc.com/news/news_structure/"
    #     file_name = spark.read.format("csv").option("header","true").load("hdfs://ip-10-164-161-34.ec2.internal:8020/user/bhanuprakash_adapa/csv/analyst_topic_ticker_df.csv")
    #     #file_name.show()

    ## LOAD MAPPINGS NEEDED FOR PROCESSING NEWS
    ## Need mapping of MI news topics to ModelDevelop news topics
    file_name = "hdfs://ip-10-164-161-34.ec2.internal:8020/user/bhanuprakash_adapa/csv/MI_Discovery_Event_Mapping.csv"
    # mi_discovery_event_mapping = pd.read_csv(file_name,sep='|')
    mi_discovery_event_mapping = spark.read.format("csv").option("header", "true").option("delimiter", "|").load(
        file_name)

    ## Need mapping of ModelDevelop news topics to alert criteria
    file_name = "hdfs://ip-10-164-161-34.ec2.internal:8020/user/bhanuprakash_adapa/csv/news_topic_alert_criteria.csv"
    alert_criteria = spark.read.format("csv").option("header", "true").option("delimiter", "|").load(file_name)

    ## Need mapping of ModelDevelop news topics to affected subscores
    file_name = "hdfs://ip-10-164-161-34.ec2.internal:8020/user/bhanuprakash_adapa/csv/news_topic_affected_subscore_criteria.csv"
    affected_subscores_criteria = spark.read.format("csv").option("header", "true").option("delimiter", "|").load(
        file_name)

    ## Need mapping of topic to analyst in order to use specific model
    file_name = "hdfs://ip-10-164-161-34.ec2.internal:8020/user/bhanuprakash_adapa/csv/analyst_topic_ticker_df.csv"
    analyst_topic_ticker = spark.read.format("csv").option("header", "true").load(file_name)
    # logging.debug('Total rows from analyst data: %s rows with %s unique topics', len(analyst_topic_ticker),len(analyst_topic_ticker['topic'].unique()))

    ## Create dmap to merge eid/cid/topic/sector/etc info with news
    #  Drop analyst column and remove any duplicates for topic/company mapping

    #     affected_subscores_criteria.show()
    #     mi_discovery_event_mapping.show()

    dmap = analyst_topic_ticker.drop('analyst').drop_duplicates()
    # dmap.show()

    # logging.debug('Load news data from Google and pre-process')

    start_date = '2018-08-14'

    # df = prepare_google_news_df(raw_df)

    df = dmap.withColumn("sector", dmap.subsector)

    dmap = dmap.withColumn("sector", dmap.subsector).limit(10)

    print('Google News stories prepared')

    # dmap.show()

    # df = df.merge(dmap.loc[:,['topic','ticker','cid','sector','subsector']],how='left',on='topic')

    df1 = df.join(dmap.select('topic', 'ticker', 'eid', 'sector', 'subsector'), df.topic == dmap.topic, "left")
    # df.show()

    # df['subsector_topic'] = np.where(df['subsector']=='OILGASEXPP','OPEC','AI')

    df = df.filter("subsector in ('OILGASEXPP','OPEC','AI')")
    # df.show()
    df = df.withColumn("cid", df.eid).withColumn("mi_event_types", F.lit("mi_event")).withColumn("mi_role_types",
                                                                                                 F.lit("mi_role"))
    fillna_values = {'ticker': '', 'eid': '', 'cid': '', 'subsector': '', 'mi_event_types': '', 'mi_role_types': ''}
    df.fillna(value=fillna_values)
    # df.show()
    # analyst_topic_ticker.show()

    # b = NewsTopicModel()
    #     topic_df = pd.DataFrame()
    #     logging.debug('Running Topic Classification')

    dict_list = map(lambda row: row.asDict(), df.collect())

    for i in dict_list:
        print(str(i))


if __name__=="__main__":
    print("Bahniu12")
    main()
    tm.testing()
