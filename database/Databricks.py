from databricks import sql
import re
import calendar
import pandas as pd
import os
from collections import namedtuple

import datetime
from datetime import datetime, timedelta
import signal
import allure
from pyspark.sql import Row
from collections import defaultdict
import csv
from collections import defaultdict, namedtuple
from collections import defaultdict
from contextlib import contextmanager
from collections import namedtuple
from selenium.common import TimeoutException
from ev import EV


def connect_to_databricks():
    print("Trying to connect to Databricks...")
    os.environ['SSL_CERT_FILE'] = EV.os
    try:
        connection = sql.connect(server_hostname=EV.host,
                                 http_path=EV.http,
                                 access_token=EV.access_token,
                                 catalog=EV.catalog)
        print("Connected to Databricks!")
        return connection
    except Exception as e:
        print("An error occurred while connecting to the Databricks:", e)
        return None


class Databricks:
    def __init__(self):
        self.client0 = connect_to_databricks()
        self.unique_transaction_id_count1 = 0
        self.unique_transaction_id_count = 0
        self.total_calls_at_11 = 0

    class TimeoutException(Exception):
        pass

    # def execute_query_invoices(self):
    #     print("Starting to execute the query...")
    #     query = "SELECT DISTINCT master.id, master.CompanyName, master.CompanyCode, master.Active FROM voyce.company as master"
    #     try:
    #         print("Trying to fetch data...")
    #         with self.client0.cursor() as cursor:
    #             cursor.execute(query)
    #             result = cursor.fetchall()
    #
    #             id_counts = {}  # for counting the occurrence of each Id
    #             total_service_minutes = 0  # for summing up ServiceMinutes
    #             serviced_count = 0  # for counting occurrences of 'Serviced' status
    #             pending_count = 0  # for counting occurrences of 'Pending' status
    #             in_service_count = 0  # for counting occurrences of 'In Service' status
    #             cancelled_count = 0
    #             new_count = 0
    #
    #             # New code to count the number of rows returned by the query
    #             row_count = len(result)
    #             print(f"Number of rows returned by the query: {row_count}")
    #
    #             for row in result:
    #                 # # accounting for each Id
    #                 # id_counts[row['ReferenceTransactionId']] = id_counts.get(row['ReferenceTransactionId'], 0) + 1
    #                 #
    #                 # # check ServiceMinutes value before adding to the counter
    #                 # if row['ServiceMinutes'] is not None:
    #                 #     total_service_minutes += row['ServiceMinutes']
    #                 #
    #                 # # check each row for the status "Serviced"
    #                 # if row['Status'] == 'Serviced':
    #                 #     serviced_count += 1
    #                 #
    #                 # # check each row for the status "Pending"
    #                 # if row['Status'] == 'Pending':
    #                 #     pending_count += 1
    #                 #
    #                 # # check each row for the status "Pending"
    #                 # if row['Status'] == 'Cancelled':
    #                 #     cancelled_count += 1
    #                 #
    #                 # if row['Status'] == 'New':
    #                 #     new_count += 1
    #                 #
    #                 # # check each row for the status "In Service"
    #                 # if row['Status'] == 'In Service':
    #                 #     in_service_count += 1
    #                 print(row)
    #
    #             print("Data fetched successfully!")
    #             # print(f"Number of 'Serviced' status: {serviced_count}")
    #             # print(f"Number of 'Pending' status: {pending_count}")
    #             # print(f"Number of 'In Service' status: {in_service_count}")
    #             # print(f"Number of 'Cancelled' status: {cancelled_count}")
    #             # print(f"Number of 'New' status: {new_count}")
    #
    #             # duplicate_ids = {k: v for k, v in id_counts.items() if v > 1}
    #
    #             # print(f"Duplicate Ids: {duplicate_ids}")  # printing the duplicate Ids
    #             # print(f"Total Service Minutes: {total_service_minutes}")  # printing the total ServiceMinutes
    #
    #     except Exception as e:
    #         print("An error occurred while executing the Databricks query:", e)
    #

    def all_companies(self):
        print("Starting to execute the query...")
        query = "select * from voyce.company"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_invoices2023(self):
        print("Starting to execute the query...")
        query = "SELECT master.Id AS InvoiceMasterId, invoice.InvoiceTxnDate AS TxnDate, invoice.InvoiceCustomerRef.name AS CustomerName, invoice.InvoiceTotalAmt AS TotalAmt, invoice.InvoiceCurrencyRef.value AS Currency, invoice.InvoiceDueDate AS DueDate, invoice.PaymentTxnDate AS PaymentDate, invoice.Status AS invoiceStatus FROM voyce.invoicemaster AS master INNER JOIN voyce.invoicemasterquickbook AS qb ON qb.InvoiceMasterId = master.Id INNER JOIN voyce.qb_invoices_new AS invoice ON invoice.InvoiceId = qb.InvoiceQuickbookId WHERE master.RowDate >= '2022-12-31' AND master.BillToRealCompanyId = 1604 AND master.RowDate <= '2023-12-31' AND invoice.Status NOT ILIKE 'voided';"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_invoices2024(self):
        print("Starting to execute the query...")
        query = "SELECT master.Id AS InvoiceMasterId, invoice.InvoiceTxnDate AS TxnDate, invoice.InvoiceCustomerRef.name AS CustomerName, invoice.InvoiceTotalAmt AS TotalAmt, invoice.InvoiceCurrencyRef.value AS Currency, invoice.InvoiceDueDate AS DueDate, invoice.PaymentTxnDate AS PaymentDate, invoice.Status AS invoiceStatus FROM voyce.invoicemaster AS master INNER JOIN voyce.invoicemasterquickbook AS qb ON qb.InvoiceMasterId = master.Id INNER JOIN voyce.qb_invoices_new AS invoice ON invoice.InvoiceId = qb.InvoiceQuickbookId WHERE master.RowDate >= '2023-12-31' AND master.RowDate <= '2024-12-31' AND master.BillToRealCompanyId = 1604  AND invoice.Status NOT ILIKE 'voided';"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # for row in result:
                #     print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_lang_rep1(self):
        print("Starting to execute the query...")
        query = "SELECT DISTINCT lang.EnglishName as TargetLanguage FROM voyce.serviceitemmaster as master INNER JOIN voyce.serviceitemdetail as child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.language as lang ON lang.Id = child.TargetLanguageId WHERE master.RequestCompanyId = 1604 and master.ClientId = 51378 order by TargetLanguage Desc;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                #     print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_lang_rep(self):
        print("Starting to execute the query...")
        query = "SELECT DISTINCT lang.EnglishName as TargetLanguage FROM voyce.serviceitemmaster as master INNER JOIN voyce.serviceitemdetail as child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.language as lang ON lang.Id = child.TargetLanguageId WHERE master.RequestCompanyId = 1604 order by TargetLanguage Desc;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                #     print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_language_stats(self, language):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=4, minute=0, second=0, microsecond=0)
        query = f"SELECT sum(a.ServiceMinutes) as ServiceMinutes, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.CountPendingAudioCalls) as CountPendingAudioCalls, sum(a.CountPendingVideoCalls) as CountPendingVideoCalls, sum(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, sum(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, sum(a.CountNewAudioCalls) as CountNewAudioCalls, sum(a.CountNewVideoCalls) as CountNewVideoCalls, sum(a.CountBackupCalls) as CountBackupCalls, sum(a.BackupWaitingSeconds) as BackupWaitingSeconds, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls FROM voyce.aggbyclienthour as a WHERE a.CompanyId = '1604' and a.DateTime >= '{now}' and a.TargetLanguage ILIKE '%{language}%'"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print(f"An error occurred while executing the query for {language}: {e}")
            return None

    def query_language_stats_CHH(self, language):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        query = f"SELECT sum(a.ServiceMinutes) as ServiceMinutes, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.CountPendingAudioCalls) as CountPendingAudioCalls, sum(a.CountPendingVideoCalls) as CountPendingVideoCalls, sum(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, sum(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, sum(a.CountNewAudioCalls) as CountNewAudioCalls, sum(a.CountNewVideoCalls) as CountNewVideoCalls, sum(a.CountBackupCalls) as CountBackupCalls, sum(a.BackupWaitingSeconds) as BackupWaitingSeconds, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls FROM voyce.aggbyclienthour as a WHERE a.CompanyId = 1604 and a.DateTime >= '{now}' AND a.TargetLanguage ILIKE '%{language}%' and a.ClientId = 51378;"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result

        except Exception as e:
            print(f"An error occurred while executing the query for")
            return None

    def query_hud_qa(self):
        now = datetime.now()  # Текущее время
        query = f"SELECT main.Id AS InterpreterId, ANY_VALUE(main.Name) AS FirstName, ANY_VALUE(main.LastName) AS LastName, ANY_VALUE(main.CreateDate) AS InterpreterJoinDate, ANY_VALUE(c.CompanyCode) AS CompanyCode, ANY_VALUE(c.Id) AS CompanyId, CASE WHEN ANY_VALUE(txn.RequestId) IS NOT NULL THEN 'In conference' WHEN ANY_VALUE(pos.ProviderOnlineStatusCodeId) = 1 THEN 'Online' ELSE 'Offline' END AS Status, ANY_VALUE(txn.RequestId) AS RequestId, ARRAY_DISTINCT(ARRAY_UNION(COLLECT_SET(lang1.EnglishName), COLLECT_SET(lang2.EnglishName))) AS Languages FROM voyce.provider AS main INNER JOIN voyce.providerservice AS service ON main.Id = service.ProviderId INNER JOIN voyce.Language AS lang1 ON service.LanguageId1 = lang1.Id INNER JOIN voyce.Language AS lang2 ON service.LanguageId2 = lang2.Id LEFT JOIN voyce.lspprovider AS lsp ON main.Id = lsp.ProviderId LEFT JOIN voyce.company AS c ON lsp.CompanyId = c.Id LEFT JOIN (SELECT child.RequestId, child.ProviderId FROM voyce.serviceitemdetail AS child INNER JOIN voyce.request AS req ON child.RequestId = req.Id INNER JOIN voyce.serviceitemmaster AS master ON master.Id = child.ServiceItemMasterId WHERE req.RequestStatusCodeId IN (1, 2)) AS txn ON txn.ProviderId = main.Id LEFT JOIN (SELECT pos.*, ROW_NUMBER() OVER (PARTITION BY pos.ProviderId ORDER BY pos.LastUpdate DESC) AS rn FROM voyce.provideronlinestatus AS pos) AS pos ON pos.ProviderId = main.Id AND pos.rn = 1 WHERE main.Available = true AND service.Deleted = false AND service.Active = true AND main.Name NOT ILIKE '%test%' AND main.LastName NOT ILIKE '%test%' GROUP BY main.Id"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)

                # Запись данных в файл
                with open('query_results.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)

                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_language_stats_CHH1(self, language, time_period, timeout_duration=60):
        now = datetime.now()
        safe_language = language.replace("'", "''")

        if time_period == 'yesterday':
            yesterday_start = (now - timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0)
            yesterday_end = now.replace(hour=4, minute=0, second=0, microsecond=0)
            date_condition = f"a.DateTime >= '{yesterday_start.strftime('%Y-%m-%d %H:%M:%S')}' AND a.DateTime < '{yesterday_end.strftime('%Y-%m-%d %H:%M:%S')}'"

        elif time_period == 'this_week':
            start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            date_condition = f"a.DateTime >= '{start_of_week.strftime('%Y-%m-%d %H:%M:%S')}'"


        elif time_period == 'last_week':
            start_of_last_week = (now - timedelta(days=now.weekday() + 7)).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_week = start_of_last_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
            date_condition = f"a.DateTime >= '{start_of_last_week.strftime('%Y-%m-%d %H:%M:%S')}' AND a.DateTime <= '{end_of_last_week.strftime('%Y-%m-%d %H:%M:%S')}'"


        elif time_period == 'this_month':
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            date_condition = f"a.DateTime >= '{start_of_month.strftime('%Y-%m-%d %H:%M:%S')}'"

        elif time_period == 'last_30_days':
            thirty_days_ago = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
            date_condition = f"a.DateTime >= '{thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')}'"


        elif time_period == 'last_month':
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_month = start_of_last_month + timedelta(
                days=(now.replace(day=1) - start_of_last_month).days - 1, hours=23, minutes=59, seconds=59)
            date_condition = f"a.DateTime >= '{start_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}' AND a.DateTime <= '{end_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}'"

        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            date_condition = f"a.DateTime >= '{start_of_year.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_year':
            start_of_last_year = (
                now.replace(year=now.year - 1, month=1, day=1, hour=-0, minute=0, second=0, microsecond=0))
            end_of_last_year = now.replace(month=1, day=1, hour=0, minute=0, second=0,
                                           microsecond=0)  # Конец предыдущего года за одну секунду до 06:00:00 первого января текущего года
            date_condition = f"a.DateTime >= '{start_of_last_year.strftime('%Y-%m-%d %H:%M:%S')}' AND a.DateTime < '{end_of_last_year.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время  # В случае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"""SELECT sum(a.ServiceMinutes) as ServiceMinutes, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.CountPendingAudioCalls) as CountPendingAudioCalls, sum(a.CountPendingVideoCalls) as CountPendingVideoCalls, sum(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, sum(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, sum(a.CountNewAudioCalls) as CountNewAudioCalls, sum(a.CountNewVideoCalls) as CountNewVideoCalls, sum(a.CountBackupCalls) as CountBackupCalls, sum(a.BackupWaitingSeconds) as BackupWaitingSeconds, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls FROM voyce.aggbyclienthour as a WHERE a.CompanyId = 1604 and {date_condition} AND a.TargetLanguage ILIKE '%{safe_language}%' and a.ClientId = 51378;"""

        signal.signal(signal.SIGALRM, Databricks.timeout_handler)
        signal.alarm(timeout_duration)  # установка таймаута

        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Databricks.TimeoutException:
            raise RuntimeError(
                f"Query timed out for language {language} and period {time_period}. Time limit of {timeout_duration} seconds exceeded.")
        except Exception as e:
            print(f"An error occurred while executing the query for {language}: {e}")
            return None
        finally:
            signal.alarm(0)  # сброс таймаута

    def timeout_handler(signum, frame):
        raise Databricks.TimeoutException()

    def query_language_stats_CHH12(self, language, time_period, timeout_duration=60):
        now = datetime.now() - timedelta(hours=6)
        safe_language = language.replace("'", "''")
        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday = now - timedelta(days=1)
            date_condition = f"a.DateTime = '{yesterday.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_week':
            start_of_week = (now - timedelta(days=now.weekday())).replace(hour=6, minute=0, second=0, microsecond=0)
            date_condition = f"a.DateTime >= '{start_of_week.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_week':
            start_of_last_week = (now - timedelta(days=now.weekday() + 7)).replace(hour=1, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_week = start_of_last_week + timedelta(days=7)
            date_condition = f"a.DateTime >= '{start_of_last_week.strftime('%Y-%m-%d')}' AND a.DateTime <= '{end_of_last_week.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"a.DateTime >= '{start_of_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_30_days':
            thirty_days_ago = now - timedelta(days=30)
            date_condition = f"a.DateTime >= '{thirty_days_ago.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_month':
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=6, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_month = now.replace(day=1, hour=6, minute=0, second=0, microsecond=0) - timedelta(days=1)
            date_condition = f"a.DateTime >= '{start_of_last_month.strftime('%Y-%m-%d')}' AND a.DateTime < '{end_of_last_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1, hour=6)
            date_condition = f"a.DateTime >= '{start_of_year.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_year':
            start_of_last_year = (now.replace(year=now.year - 1, month=1, day=1, hour=6))
            end_of_last_year = now.replace(month=1, day=1)
            date_condition = f"a.DateTime >= '{start_of_last_year.strftime('%Y-%m-%d')}' AND a.DateTime <= '{end_of_last_year.strftime('%Y-%m-%d')}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"""SELECT sum(a.ServiceMinutes) as ServiceMinutes, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.CountPendingAudioCalls) as CountPendingAudioCalls, sum(a.CountPendingVideoCalls) as CountPendingVideoCalls, sum(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, sum(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, sum(a.CountNewAudioCalls) as CountNewAudioCalls, sum(a.CountNewVideoCalls) as CountNewVideoCalls, sum(a.CountBackupCalls) as CountBackupCalls, sum(a.BackupWaitingSeconds) as BackupWaitingSeconds, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls FROM voyce.aggbyclienthour as a WHERE a.CompanyId = 1604 and {date_condition} AND a.TargetLanguage ILIKE '%{safe_language}%' and a.ClientId = 51378;"""

        signal.signal(signal.SIGALRM, Databricks.timeout_handler)
        signal.alarm(timeout_duration)  # установка таймаута

        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result
        except Databricks.TimeoutException:
            raise RuntimeError(
                f"Query timed out for language {language} and period {time_period}. Time limit of {timeout_duration} seconds exceeded.")
        except Exception as e:
            print(f"An error occurred while executing the query for {language}: {e}")
            return None
        finally:
            signal.alarm(0)  # сброс таймаута

    def query_ASC(self):
        print("Starting to execute the query...")
        query = "SELECT DISTINCT lang.EnglishName as TargetLanguage FROM voyce.serviceitemmaster as master INNER JOIN voyce.serviceitemdetail as child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.language as lang ON lang.Id = child.TargetLanguageId WHERE master.RowDate > current_date() - 1 and master.RequestCompanyId = 1090 order by TargetLanguage ASC;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                # print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_lang_DESC(self):
        print("Starting to execute the query...")
        query = "SELECT DISTINCT lang.EnglishName as TargetLanguage FROM voyce.serviceitemmaster as master INNER JOIN voyce.serviceitemdetail as child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.language as lang ON lang.Id = child.TargetLanguageId WHERE master.RowDate = current_date() - 1 and master.RequestCompanyId = 1090 order by TargetLanguage Desc;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                # print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_ASC1(self):
        print("Starting to execute the query...")
        query = "SELECT DISTINCT lang.EnglishName as TargetLanguage FROM voyce.serviceitemmaster as master INNER JOIN voyce.serviceitemdetail as child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.language as lang ON lang.Id = child.TargetLanguageId WHERE master.RowDate = current_date() - 1 and master.RequestCompanyId = 1090 order by TargetLanguage ASC;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                # print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_lang_DESC1(self):
        print("Starting to execute the query...")
        query = "SELECT DISTINCT lang.EnglishName as TargetLanguage FROM voyce.serviceitemmaster as master INNER JOIN voyce.serviceitemdetail as child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.language as lang ON lang.Id = child.TargetLanguageId WHERE master.RowDate = current_date() - 1 and master.RequestCompanyId = 1090 order by TargetLanguage Desc;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                # print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_total_calls(self):
        print("Starting to execute the query...")
        query = "SELECT a.TargetLanguage, sum(a.ServiceMinutes) as ServiceMinutes, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.CountPendingAudioCalls) as CountPendingAudioCalls, sum(a.CountPendingVideoCalls) as CountPendingVideoCalls, sum(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, sum(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, sum(a.CountNewAudioCalls) as CountNewAudioCalls, sum(a.CountNewVideoCalls) as CountNewVideoCalls, sum(a.CountBackupCalls) as CountBackupCalls, sum(a.BackupWaitingSeconds) as BackupWaitingSeconds, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls FROM voyce.aggbyclienthour as a WHERE a.CompanyId = 1090 and a.Date > CURRENT_DATE() - 1 GROUP by a.TargetLanguage;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                language_quantity = len(result)  # Подсчет количества уникальных языков
                print(f"Total unique languages: {language_quantity}")  # Вывод количества уникальных языков
                # for row in result:
                # print(row)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_NM(self):
        print("Starting to execute the query...")

        today_date_str = datetime.now().strftime('%Y-%m-%d 05:00:00')
        # print(today_date_str)
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE master.RequestTime >= '{today_date_str}' AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL ORDER BY ClientSite, IOSSerialNumber"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Yale(self):
        print("Starting to execute the query...")

        today_date_str = datetime.now().strftime('%Y-%m-%d 05:00:00')
        # print(today_date_str)
        query = f"SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds / 60) AS ServiceMinutes, master.RequestTime AS RequestTime, DATE_FORMAT(master.RequestTime, 'HH:mm:ss') AS ExtractedTime, timezone.TimeZoneId AS Timezone, master.ClientUserId AS UserId, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN (master.CallerId IS NULL OR master.CallerId = '') THEN 'Application' ELSE master.CallerId END AS CallerID, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status, (SELECT ARRAY_AGG(STRUCT(inputs.DataInputName AS Name, inputs.DataInputValue AS Value)) FROM voyce.serviceitemdatainput AS inputs WHERE inputs.ServiceItemDetailId = child.Id) AS intakeQuestions, i.DataInputValue AS Site FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId INNER JOIN voyce.company AS c ON c.Id = master.RequestCompanyId LEFT JOIN voyce.requesteval AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE master.RequestTime >= '{today_date_str}' AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND lang.EnglishName NOT ILIKE '%Operator%' AND master.RequestCompanyId = 1899 ORDER BY master.RequestTime DESC LIMIT 100 OFFSET 0;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Indiana(self):
        print("Starting to execute the query...")

        # Генерация строки текущей даты с временем 05:00:00
        today_date_str = datetime.now().strftime('%Y-%m-%d 05:00:00')

        query = f"SELECT ANY_VALUE(master.RequestId) AS referencetransactionid, q2.PropertyValue AS IOSSerialNumber, ANY_VALUE(master.RequestTime) AS RequestTime, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes, ANY_VALUE(master.ClientId) as ClientId, ANY_VALUE(master.RequestCompanyId) as CompanyId, COUNT(*) AS NumberOfServices FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE NOT ISNULL(q2.PropertyValue) AND NOT ISNULL(master.RequestId) AND NOT ISNULL(master.RequestTime) AND NOT ISNULL(master.ClientId) AND NOT ISNULL(master.RequestCompanyId) AND master.RequestTime >= '{today_date_str}' AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1604 GROUP BY q2.PropertyValue HAVING IOSSerialNumber is not null"

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_tr_p_last_year(self):
        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)

        # Первое число текущего месяца
        start = now.replace(year=now.year - 1, month=1, day=1)
        end = now.replace(month=1, day=1)
        date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime <= '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        print(start)
        print(end)

        # Составление запроса
        query = "select * from ((select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster_historic as master inner join voyce.serviceitemdetail_historic as child on master.id = child.ServiceItemMasterId inner join voyce.request_historic as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval_historic as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where " + date_condition + " and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1604 order by master.RequestTime desc) UNION ALL (select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where " + date_condition + " and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1604 order by master.RequestTime desc)) order by RequestTime desc"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                # Запись данных в файл
                with open('query_results_last_YEAR.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)

                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_tr_p_last_month(self):
        now = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)

        # Первое число текущего месяца
        start_current_month = now.replace(day=1)

        # Первое число прошлого месяца
        start_previous_month = (start_current_month - timedelta(days=1)).replace(day=1)

        # Условие для запроса на начало прошлого месяца
        date_condition_start_previous_month = f"master.RequestTime >= '{start_previous_month.strftime('%Y-%m-%d %H:%M:%S')}'"

        # Условие для запроса на начало текущего месяца
        date_condition_start_current_month = f"master.RequestTime < '{start_current_month.strftime('%Y-%m-%d %H:%M:%S')}'"

        print(start_current_month)
        print(start_previous_month)

        # Составление запроса
        query = "select * from ((select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster_historic as master inner join voyce.serviceitemdetail_historic as child on master.id = child.ServiceItemMasterId inner join voyce.request_historic as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval_historic as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where " + date_condition_start_previous_month + " and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1604 order by master.RequestTime desc) UNION ALL (select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where " + date_condition_start_current_month + " and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1604 order by master.RequestTime desc)) order by RequestTime desc"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                # Запись данных в файл
                with open('query_results_last_month.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)

                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def find_absolute_duplicates(self, result):
        records_count = defaultdict(int)

        # Подсчитываем количество вхождений для каждой записи
        for record in result:
            # Используем именно идентификатор RequestId в качестве ключа, а не всю запись
            request_id = record['RequestId']
            records_count[request_id] += 1

        # Выбираем записи, которые встречаются более одного раза
        absolute_duplicates = {request_id for request_id, count in records_count.items() if count > 1}

        return absolute_duplicates

    def find_absolute_duplicates1(self, result):
        records_count = defaultdict(int)

        # Подсчитываем количество вхождений для каждой записи
        for record in result:
            # Используем именно идентификатор RequestId в качестве ключа, а не всю запись
            request_id = record['ReferenceTransactionId']
            records_count[request_id] += 1

        # Выбираем записи, которые встречаются более одного раза
        absolute_duplicates = {request_id for request_id, count in records_count.items() if count > 1}

        return absolute_duplicates

    def print_transaction_ids_info(self, unique_ids, duplicate_ids, absolute_duplicates):
        print(f"Number of unique transaction IDs: {len(unique_ids)}")
        print(f"Number of duplicate transaction IDs: {len(duplicate_ids)}")
        if duplicate_ids:
            # Преобразуем set в строку для вывода
            print(f"Duplicate transaction IDs: {', '.join(str(dup) for dup in duplicate_ids)}")
        print(f"Number of absolute duplicates: {len(absolute_duplicates)}")
        if absolute_duplicates:
            print("Absolute duplicates:")
            # Предполагаем, что absolute_duplicates - это просто идентификаторы
            for duplicate in absolute_duplicates:
                print(duplicate)

    def query_transactions_periods_Admin(self, time_period):
        print("Starting to execute the query for the time period:", time_period)

        now = datetime.now()
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Убедитесь, что время установлено корректно
        now2 = '2024-08-28 00:00:00'
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')

        # Инициализируем start значением по умолчанию
        start = now.replace(day=1)

        if time_period == 'yesterday':
            start = now - timedelta(days=1)
            end = now
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_week':
            start = now - timedelta(days=now.weekday())
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_week':
            start = now - timedelta(days=now.weekday() + 7)
            end = start + timedelta(days=7)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime <= '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_month':
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_30_days':
            start = now - timedelta(days=30)
            end = now
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_year':
            start = now.replace(month=1, day=1)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
            print(start)
        elif time_period == 'last_month':
            start_current_month = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)
            start_previous_month = (start_current_month - timedelta(days=1)).replace(day=1, hour=5, minute=0, second=0,
                                                                                     microsecond=0)
            end_previous_month = start_current_month  # Уже установлено в 2024-03-01 04:00:00

            print(start_previous_month)
            print(end_previous_month)
            date_condition = f"master.RequestTime >= '{start_previous_month.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime <= '{end_previous_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_year':
            start = now.replace(year=now.year - 1, month=1, day=1)
            end = now.replace(year=now.year, month=1, day=1)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            # В случае неизвестного периода, запрос возвращает данные за все время
            date_condition = "1=1"

        print("Time period from:", start.strftime('%Y-%m-%d %H:%M:%S'), "to current time")
        query = f"""
                    SELECT 
                        HOUR(FROM_UTC_TIMESTAMP(child.RequestTime, 'America/New_York')) AS Hour,
                        master.RequestTime AS RequestTime,
                        child.RequestId AS RequestId,
                        master.RequestCompanyId AS CompanyId,
                        master.ClientId AS ClientId,
                        lang.EnglishName AS Language,
                        lang.Id AS LanguageId,
                        master.IsVideo AS IsVideo,
                        CEIL((child.ServiceSeconds)/60) AS ServiceMinutes,
                        child.WaitSeconds AS WaitSeconds,
                        eva.Answer AS Rating,
                        CEIL(rp.TotalPrice) AS TotalPrice,
                        CASE WHEN eva.Answer IS NOT NULL THEN 1 ELSE 0 END AS RatedCalls,
                        CASE master.IsVideo WHEN true THEN 'Video' ELSE 'Audio' END AS CallType,
                        CASE master.IsVideo WHEN true THEN CEIL((child.ServiceSeconds)/60) ELSE 0 END AS VideoMinutes,
                        CASE master.IsVideo WHEN false THEN CEIL((child.ServiceSeconds)/60) ELSE 0 END AS AudioMinutes,
                        CASE master.IsVideo WHEN true THEN 1 ELSE 0 END AS VideoCall,
                        CASE master.IsVideo WHEN false THEN 1 ELSE 0 END AS AudioCall,
                        CASE master.RoutedToBackup WHEN true THEN 1 ELSE 0 END AS BackupCall,
                        CASE WHEN lang.Id = 44 THEN 1 ELSE 0 END AS SpanishCall,
                        CASE WHEN lang.Id = 44 THEN child.WaitSeconds ELSE 0 END AS SpanishWaitSeconds,
                        CASE WHEN lang.Id != 44 THEN 1 ELSE 0 END AS LotsCall,
                        CASE WHEN lang.Id != 44 THEN child.WaitSeconds ELSE 0 END AS LotsWaitSeconds,
                        CASE 
                            WHEN req.RequestStatusCodeId = 1 THEN "New"
                            WHEN req.RequestStatusCodeId = 2 THEN "In Service"
                            ELSE CASE
                                WHEN master.ServiceItemStatusCodeId = 3 THEN "Pending"
                                ELSE CASE
                                    WHEN child.ServiceSeconds > 0 THEN "Serviced"
                                    ELSE "Cancelled"
                                END
                            END
                        END AS Status
                    FROM 
                        voyce.serviceitemmaster AS master 
                    INNER JOIN 
                        voyce.serviceitemdetail AS child ON child.ServiceItemMasterId = master.Id
                    INNER JOIN 
                        voyce.request AS req ON req.Id = child.RequestId
                    INNER JOIN 
                        voyce.language AS lang ON lang.Id = child.TargetLanguageId
                    LEFT JOIN 
                        voyce.requesteval AS eva ON eva.RequestId = req.Id AND EvalQuestionId = 1
                    LEFT JOIN 
                        voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId
                    WHERE 
                        {date_condition}
                    ORDER BY
                        master.RequestTime DESC
                    """
        try:
            print("Попытка извлечь данные...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                unique_ids = set()
                duplicate_ids = set()
                records = []

                for record in result:
                    records.append(record)
                    transaction_id = record['RequestId']
                    if transaction_id in unique_ids:
                        duplicate_ids.add(transaction_id)
                    else:
                        unique_ids.add(transaction_id)

                absolute_duplicates = self.find_absolute_duplicates(records)

                # Вызов функции print_transaction_ids_info с информацией о дубликатах
                self.print_transaction_ids_info(unique_ids, duplicate_ids, absolute_duplicates)

                # Далее следует ваш код для обработки результатов запроса
                # Например, запись результатов в файл
                with open('query_results_ADM.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)
                return result

        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def query_transactions_periods(self, time_period):
        print("Starting to execute the query for the time period:", time_period)

        now = datetime.now()
        now = now.replace(hour=4, minute=0, second=0, microsecond=0)

        # Инициализируем start значением по умолчанию
        start = now.replace(day=1)

        # Определение начальной и конечной даты в зависимости от time_period
        if time_period == 'yesterday':
            start = now - timedelta(days=1)
            end = now
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_week':
            start = now - timedelta(days=now.weekday())
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_week':
            start = now - timedelta(days=now.weekday() + 7)
            end = start + timedelta(days=7)
            print(start)
            print(end)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime <= '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_month':
            start = now.replace(day=1)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_30_days':
            start = now - timedelta(days=30)
            end = now
            print(start)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_year':
            start = now.replace(month=1, day=1)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            # В случае неизвестного периода, запрос возвращает данные за все время
            date_condition = "1=1"

        print("Time period from:", start.strftime('%Y-%m-%d %H:%M:%S'), "to current time")
        query = f"SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds/60) AS ServiceMinutes, master.RequestTime AS RequestTime, DATE_FORMAT(master.RequestTime, 'HH:mm:ss') AS ExtractedTime, timezone.TimeZoneId AS Timezone, master.ClientUserId AS UserId, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN (master.CallerId IS NULL OR master.CallerId = '') THEN 'Application' ELSE master.CallerId END AS CallerID, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId LEFT JOIN voyce.requesteval AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId WHERE {date_condition} AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND lang.EnglishName NOT ILIKE '%Operator%' AND master.RequestCompanyId = 1604 UNION ALL SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds/60) AS ServiceMinutes, master.RequestTime AS RequestTime, DATE_FORMAT(master.RequestTime, 'HH:mm:ss') AS ExtractedTime, timezone.TimeZoneId AS Timezone, master.ClientUserId AS UserId, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN (master.CallerId IS NULL OR master.CallerId = '') THEN 'Application' ELSE master.CallerId END AS CallerID, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId LEFT JOIN voyce.requesteval_historic AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId WHERE {date_condition} AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND lang.EnglishName NOT ILIKE '%Operator%' AND master.RequestCompanyId = 1604 ORDER BY RequestTime DESC;"
        try:
            print("Попытка извлечь данные...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                unique_ids = set()
                duplicate_ids = set()
                records = []

                for record in result:
                    records.append(record)
                    transaction_id = record['ReferenceTransactionId']
                    if transaction_id in unique_ids:
                        duplicate_ids.add(transaction_id)
                    else:
                        unique_ids.add(transaction_id)

                absolute_duplicates = self.find_absolute_duplicates1(records)

                # Вызов функции print_transaction_ids_info с информацией о дубликатах
                self.print_transaction_ids_info(unique_ids, duplicate_ids, absolute_duplicates)

                # Далее следует ваш код для обработки результатов запроса
                # Например, запись результатов в файл
                with open('query_results_CUSTOMER.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)

                return result

        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def query_transactions_periods_Admin_PROD(self, time_period):
        print("Starting to execute the query for the time period:", time_period)

        now = datetime.now()
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Убедитесь, что время установлено корректно

        # Инициализируем start значением по умолчанию
        start = now.replace(day=1)

        if time_period == 'yesterday':
            start = now - timedelta(days=1)
            end = now
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_week':
            start = now - timedelta(days=now.weekday())
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_week':
            start = now - timedelta(days=now.weekday() + 7)
            end = start + timedelta(days=7)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime <= '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_month':
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_30_days':
            start = now - timedelta(days=30)
            end = now
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_year':
            start = now.replace(month=1, day=1)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}'"
            print(start)
        elif time_period == 'last_month':
            start_current_month = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)
            start_previous_month = (start_current_month - timedelta(days=1)).replace(day=1, hour=5, minute=0, second=0,
                                                                                     microsecond=0)
            end_previous_month = start_current_month  # Уже установлено в 2024-03-01 04:00:00

            print(start_previous_month)
            print(end_previous_month)
            date_condition = f"master.RequestTime >= '{start_previous_month.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime <= '{end_previous_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_year':
            start = now.replace(year=now.year - 1, month=1, day=1)
            end = now.replace(year=now.year, month=1, day=1)
            date_condition = f"master.RequestTime >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            # В случае неизвестного периода, запрос возвращает данные за все время
            date_condition = "1=1"

        print("Time period from:", start.strftime('%Y-%m-%d %H:%M:%S'), "to current time")
        query = f"SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds/60) AS ServiceMinutes, master.RequestTime AS RequestTime, DATE_FORMAT(master.RequestTime, 'HH:mm:ss') AS ExtractedTime, timezone.TimeZoneId AS Timezone, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, from_utc_timestamp(master.RequestTime, 'America/New_York') AS tDate, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN (master.CallerId IS NULL OR master.CallerId = '') THEN 'Application' ELSE master.CallerId END AS CallerID, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp_count.RoutingHistoryLength AS RoutingHistoryLength, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId LEFT JOIN voyce.requesteval AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN (SELECT RequestId, COUNT(*) AS RoutingHistoryLength FROM voyce.requestprovider GROUP BY RequestId) AS rp_count ON rp_count.RequestId = child.RequestId WHERE {date_condition} AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 UNION ALL SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds/60) AS ServiceMinutes, master.RequestTime AS RequestTime, DATE_FORMAT(master.RequestTime, 'HH:mm:ss') AS ExtractedTime, timezone.TimeZoneId AS Timezone, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, from_utc_timestamp(master.RequestTime, 'America/New_York') AS tDate, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN (master.CallerId IS NULL OR master.CallerId = '') THEN 'Application' ELSE master.CallerId END AS CallerID, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp_count.RoutingHistoryLength AS RoutingHistoryLength, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId LEFT JOIN voyce.requesteval_historic AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN (SELECT RequestId, COUNT(*) AS RoutingHistoryLength FROM voyce.requestprovider_historic GROUP BY RequestId) AS rp_count ON rp_count.RequestId = child.RequestId WHERE {date_condition} AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 ORDER BY RequestTime DESC;"
        try:
            print("Попытка извлечь данные...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                unique_ids = set()
                duplicate_ids = set()
                records = []

                for record in result:
                    records.append(record)
                    transaction_id = record['ReferenceTransactionId']
                    if transaction_id in unique_ids:
                        duplicate_ids.add(transaction_id)
                    else:
                        unique_ids.add(transaction_id)

                absolute_duplicates = self.find_absolute_duplicates1(records)

                # Вызов функции print_transaction_ids_info с информацией о дубликатах
                self.print_transaction_ids_info(unique_ids, duplicate_ids, absolute_duplicates)

                # Далее следует ваш код для обработки результатов запроса
                # Например, запись результатов в файл
                with open('query_results_ADM.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)
                return result

        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def query_activity_m_periods(self, time_period):
        print("Starting to execute the query for time period:", time_period)

        # Логика определения временного периода
        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра

        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday = now - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{yesterday.strftime('%Y-%m-%d')}' and master.RequestTime < '{now}'"
        elif time_period == 'this_week':
            start_of_week = (now - timedelta(days=now.weekday()))
            date_condition = f"master.RequestTime >= '{start_of_week.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_week':
            start_of_last_week = (now - timedelta(days=now.weekday() + 7))
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"master.RequestTime >= '{start_of_last_week.strftime('%Y-%m-%d')}' AND master.RequestTime < '{end_of_last_week.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"master.RequestTime >= '{start_of_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_30_days':
            thirty_days_ago = now - timedelta(days=30)
            date_condition = f"master.RequestTime >= '{thirty_days_ago.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_month':
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
            end_of_last_month = now.replace(day=1) - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{start_of_last_month.strftime('%Y-%m-%d')}' AND master.RequestTime < '{end_of_last_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1)
            date_condition = f"master.RequestTime >= '{start_of_year.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_year':
            start_of_last_year = now.replace(year=now.year - 1, month=1, day=1)
            end_of_last_year = now.replace(month=1, day=1) - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{start_of_last_year.strftime('%Y-%m-%d')}' AND master.RequestTime < '{end_of_last_year.strftime('%Y-%m-%d')}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        query = f"select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case WHEN master.CallerId IS NULL OR master.CallerId = '' THEN 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' END AS Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId where {date_condition} and (req.RequestStatusCodeId = 1 OR req.RequestStatusCodeId = 2 OR (req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId = 3)) and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1604 order by master.RequestTime desc"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result  # Возвращаем результат для дальнейшей обработки
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_transactions_today(self):
        print("Starting to execute the query...")
        # Генерация строки текущей даты с временем 05:00:00
        today_date_str = datetime.now().strftime('%Y-%m-%d 04:00:00')
        print(today_date_str)

        query = f"SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds/60) AS ServiceMinutes, master.RequestTime AS RequestTime, DATE_FORMAT(master.RequestTime, 'HH:mm:ss') AS ExtractedTime, timezone.TimeZoneId AS Timezone, master.ClientUserId AS UserId, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN (master.CallerId IS NULL OR master.CallerId = '') THEN 'Application' ELSE master.CallerId END AS CallerID, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId LEFT JOIN voyce.requesteval AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId WHERE master.RequestTime >= '{today_date_str}' AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND lang.EnglishName NOT ILIKE '%Operator%' AND master.ClientId IN (49957,51037,51378,51379,51380,52864) AND master.RequestCompanyId = 1604 ORDER BY master.RequestTime DESC;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                # Подсчет уникальных ReferenceTransactionId
                unique_ids = set()
                for record in result:
                    unique_ids.add(record['ReferenceTransactionId'])

                # Сохранение количества уникальных ID в атрибут класса
                self.unique_transaction_id_count = len(unique_ids)
                print(f"Количество уникальных ReferenceTransactionId: {self.unique_transaction_id_count}")
                return result

        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def query_transactions_today_admin(self):
        print("Starting to execute the query...")
        # Генерация строки текущей даты с временем 05:00:00
        today_date_str = datetime.now().strftime('%Y-%m-%d 04:00:00')
        print(today_date_str)

        query = f"select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, from_utc_timestamp(master.RequestTime, 'America/New_York') as tDate, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, q2.PropertyValue AS IOSSerialNumber, rp_count.RoutingHistoryLength AS RoutingHistoryLength, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join ( select RequestId, count(*) as RoutingHistoryLength from voyce.requestprovider group by RequestId ) as rp_count on rp_count.RequestId = child.RequestId where master.RequestTime >= '{today_date_str}' and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 order by master.RequestTime desc;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                # Подсчет общего количества ReferenceTransactionId
                transaction_id_count = len(result)  # Предполагается, что каждая запись имеет ID

                # Сохранение количества ID в атрибут класса
                self.transaction_id_count = transaction_id_count

                self.unique_transaction_id_count1 = transaction_id_count

                print(f"Общее количество ReferenceTransactionId: {self.transaction_id_count}")

                # Запись данных в файл
                with open('query_results_ADMIN.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)

                return result

        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def query_activity_m(self):
        print("Starting to execute the query...")
        # Генерация строки текущей даты с временем 05:00:00
        today_date_str = datetime.now().strftime('%Y-%m-%d 00:00:00')

        query = f"select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case WHEN master.CallerId IS NULL OR master.CallerId = '' THEN 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' END AS Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId where master.RequestTime >= '{today_date_str}' and (req.RequestStatusCodeId = 1 OR req.RequestStatusCodeId = 2 OR (req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId = 3)) and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1604 order by master.RequestTime desc"

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Indiana_for_periods(self, time_period):
        print("Starting to execute the query...")

        now = datetime.now()  # Текущее время
        now = now.replace(hour=4, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра

        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday_start = now - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{yesterday_start}' AND master.RequestTime < '{now}'"
        elif time_period == 'This_week':
            # Установка начала недели на понедельник 05:00 утра
            start_of_week = (now - timedelta(days=now.weekday())).replace(hour=5, minute=0, second=0, microsecond=0)
            # Текущее время уже установлено на 05:00 утра сегодняшнего дня
            date_condition = f"master.RequestTime >= '{start_of_week}'"
        elif time_period == 'last_week':
            start_of_last_week = now - timedelta(days=now.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"master.RequestTime >= '{start_of_last_week}' AND master.RequestTime < '{end_of_last_week + timedelta(days=1)}'"
        elif time_period == 'Last_month':
            # Начало и конец последнего месяца
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=5, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_month = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)
            print("Start of Last Month:", start_of_last_month)
            print("End of Last Month:", end_of_last_month)
            date_condition = f"master.RequestTime >= '{start_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"master.RequestTime >= '{start_of_month}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"""SELECT ANY_VALUE(master.RequestId) AS referencetransactionid, q2.PropertyValue AS IOSSerialNumber, ANY_VALUE(master.RequestTime) AS RequestTime, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes, ANY_VALUE(master.ClientId) as ClientId, ANY_VALUE(master.RequestCompanyId) as CompanyId, COUNT(*) AS NumberOfServices FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE NOT ISNULL(q2.PropertyValue) AND NOT ISNULL(master.RequestId) AND NOT ISNULL(master.RequestTime) AND NOT ISNULL(master.ClientId) AND NOT ISNULL(master.RequestCompanyId) AND {date_condition} AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1604 GROUP BY q2.PropertyValue HAVING IOSSerialNumber is not null"""

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Indiana_for_last_month(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра

        start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=5, minute=0, second=0,
                                                                               microsecond=0)
        end_of_last_month = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)

        print("Start of Last Month:", start_of_last_month)
        print("End of Last Month:", end_of_last_month)

        date_condition = f"master.RequestTime >= '{start_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}'"

        # Формирование SQL-запроса с использованием исторических таблиц и date_condition
        query = f"SELECT ANY_VALUE(master.RequestId) AS referencetransactionid, q2.PropertyValue AS IOSSerialNumber, ANY_VALUE(master.RequestTime) AS RequestTime, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes, ANY_VALUE(master.ClientId) as ClientId, ANY_VALUE(master.RequestCompanyId) as CompanyId, COUNT(*) AS NumberOfServices FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE NOT ISNULL(q2.PropertyValue) AND NOT ISNULL(master.RequestId) AND NOT ISNULL(master.RequestTime) AND NOT ISNULL(master.ClientId) AND NOT ISNULL(master.RequestCompanyId) AND {date_condition} AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1604 GROUP BY q2.PropertyValue HAVING IOSSerialNumber is not null"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Indiana_for_last_30_days(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра
        start_date = now - timedelta(days=30)  # Вычисляем дату 30 дней назад

        print("Start of Last 30 Days:", start_date)
        print("End of Last 30 Days:", now)

        date_condition = f"master.RequestTime >= '{start_date.strftime('%Y-%m-%d %H:%M:%S')}'"
        # Формирование SQL-запроса с использованием date_condition
        query = f"""
        SELECT 
          ANY_VALUE(referencetransactionid) AS referencetransactionid,
          IOSSerialNumber,
          sum(ServiceMinutes) as ServiceMinutes,
          ANY_VALUE(ClientId) as ClientId,
          ANY_VALUE(CompanyId) as CompanyId,
          sum(NumberOfServices) AS NumberOfServices
        FROM (
          (
            SELECT
            ANY_VALUE(master.RequestId) AS referencetransactionid,
            q2.PropertyValue AS IOSSerialNumber,
            ANY_VALUE(master.RequestTime) AS RequestTime,
            SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes,
            ANY_VALUE(master.ClientId) as ClientId,
            ANY_VALUE(master.RequestCompanyId) as CompanyId,
            COUNT(*) AS NumberOfServices
            FROM voyce.serviceitemmaster_historic AS master
            INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request_historic as req on child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            WHERE {date_condition} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3
            AND master.RequestCompanyId = 1604
            GROUP BY q2.PropertyValue
            HAVING IOSSerialNumber is not null
          )
          UNION ALL
          (
            SELECT
            ANY_VALUE(master.RequestId) AS referencetransactionid,
            q2.PropertyValue AS IOSSerialNumber,
            ANY_VALUE(master.RequestTime) AS RequestTime,
            SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes,
            ANY_VALUE(master.ClientId) as ClientId,
            ANY_VALUE(master.RequestCompanyId) as CompanyId,
            COUNT(*) AS NumberOfServices
            FROM voyce.serviceitemmaster AS master
            INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request as req on child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            WHERE {date_condition} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3
            AND master.RequestCompanyId = 1604
            GROUP BY q2.PropertyValue
            HAVING IOSSerialNumber is not null
          )
        )
        group by IOSSerialNumber
        """
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Indiana_this_year(self):
        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)

        start_of_year = now.replace(month=1, day=1)
        formatted_start_of_year = start_of_year.strftime('%Y-%m-%d %H:%M:%S')

        # Теперь используем formatted_start_of_year в условии SQL
        date_condition = f"master.RequestTime >= '{formatted_start_of_year}'"

        # Запрос для исторических данных
        query_historic = f"""
                SELECT
                    ANY_VALUE(master.RequestId) AS referencetransactionid,
                    q2.PropertyValue AS IOSSerialNumber,
                    SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes,
                    ANY_VALUE(master.ClientId) as ClientId,
                    ANY_VALUE(master.RequestCompanyId) as CompanyId,
                    COUNT(*) AS NumberOfServices
                FROM voyce.serviceitemmaster_historic AS master
                INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId
                INNER JOIN voyce.request_historic as req on child.RequestId = req.Id
                LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId
                LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
                WHERE {date_condition} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3
                AND master.RequestCompanyId = 1604
                GROUP BY q2.PropertyValue
                HAVING IOSSerialNumber is not null
            """

        # Запрос для текущих данных
        query_current = f"""
                SELECT
                    ANY_VALUE(master.RequestId) AS referencetransactionid,
                    q2.PropertyValue AS IOSSerialNumber,
                    SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes,
                    ANY_VALUE(master.ClientId) as ClientId,
                    ANY_VALUE(master.RequestCompanyId) as CompanyId,
                    COUNT(*) AS NumberOfServices
                FROM voyce.serviceitemmaster AS master
                INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId
                INNER JOIN voyce.request as req on child.RequestId = req.Id
                LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId
                LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
                WHERE {date_condition} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3
                AND master.RequestCompanyId = 1604
                GROUP BY q2.PropertyValue
                HAVING IOSSerialNumber is not null
            """

        # Объединение запросов
        query = f"""
                SELECT 
                    ANY_VALUE(referencetransactionid) AS referencetransactionid,
                    IOSSerialNumber,
                    sum(ServiceMinutes) as ServiceMinutes,
                    ANY_VALUE(ClientId) as ClientId,
                    ANY_VALUE(CompanyId) as CompanyId,
                    sum(NumberOfServices) AS NumberOfServices
                FROM (
                    ({query_historic})
                    UNION ALL
                    ({query_current})
                )
                GROUP BY IOSSerialNumber
            """

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Indiana_last_year(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=5, minute=0, second=0,
                                     microsecond=0)  # Сейчас, но установлено время на 05:00 утра
        start_of_last_year = (now.replace(month=1, day=1, year=now.year - 1))  # Начало прошлого года
        end_of_this_year = now.replace(month=1, day=1)  # Начало текущего года

        # Форматирование дат для SQL-запроса
        formatted_start_of_last_year = start_of_last_year.strftime('%Y-%m-%d %H:%M:%S')
        formatted_end_of_this_year = end_of_this_year.strftime('%Y-%m-%d %H:%M:%S')

        # Условие для запроса первой части, использующее начало и конец последнего года
        date_condition1 = f"master.RequestTime > '{formatted_start_of_last_year}' and master.RequestTime < '{formatted_end_of_this_year}'"
        print(formatted_start_of_last_year)
        print(formatted_end_of_this_year)

        # Формирование SQL-запроса
        query = f"""
        SELECT 
          ANY_VALUE(referencetransactionid) AS referencetransactionid,
          IOSSerialNumber,
          sum(ServiceMinutes) as ServiceMinutes,
          ANY_VALUE(ClientId) as ClientId,
          ANY_VALUE(CompanyId) as CompanyId,
          sum(NumberOfServices) AS NumberOfServices
        FROM (
          (
            SELECT
            ANY_VALUE(master.RequestId) AS referencetransactionid,
            q2.PropertyValue AS IOSSerialNumber,
            ANY_VALUE(master.RequestTime) AS RequestTime,
            SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes,
            ANY_VALUE(master.ClientId) as ClientId,
            ANY_VALUE(master.RequestCompanyId) as CompanyId,
            COUNT(*) AS NumberOfServices
            FROM voyce.serviceitemmaster_historic AS master
            INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request_historic as req on child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            WHERE {date_condition1} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3
            AND master.RequestCompanyId = 1604
            GROUP BY q2.PropertyValue
            HAVING IOSSerialNumber is not null
          )
          UNION ALL
          (
            SELECT
            ANY_VALUE(master.RequestId) AS referencetransactionid,
            q2.PropertyValue AS IOSSerialNumber,
            ANY_VALUE(master.RequestTime) AS RequestTime,
            SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes,
            ANY_VALUE(master.ClientId) as ClientId,
            ANY_VALUE(master.RequestCompanyId) as CompanyId,
            COUNT(*) AS NumberOfServices
            FROM voyce.serviceitemmaster AS master
            INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request as req on child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            WHERE {date_condition1} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3
            AND master.RequestCompanyId = 1604
            GROUP BY q2.PropertyValue
            HAVING IOSSerialNumber is not null
          )
        )
        group by IOSSerialNumber;
        """

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result  # Return the result for later processing
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_NM_for_periods(self, time_period):
        print("Starting to execute the query...")

        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра

        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday_start = now - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{yesterday_start}' AND master.RequestTime <= '{now}'"
        elif time_period == 'This_week':
            # Установка начала недели на понедельник 05:00 утра
            start_of_week = (now - timedelta(days=now.weekday())).replace(hour=5, minute=0, second=0, microsecond=0)
            # Текущее время уже установлено на 05:00 утра сегодняшнего дня
            date_condition = f"master.RequestTime >= '{start_of_week}'"
        elif time_period == 'last_week':
            start_of_last_week = now - timedelta(days=now.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"master.RequestTime >= '{start_of_last_week}' AND master.RequestTime < '{end_of_last_week + timedelta(days=1)}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"master.RequestTime >= '{start_of_month}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL ORDER BY ClientSite, IOSSerialNumber"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Yale_for_periods(self, time_period):
        print("Starting to execute the query...")

        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра

        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday_start = now - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{yesterday_start}' AND master.RequestTime <= '{now}'"
        elif time_period == 'This_week':
            # Установка начала недели на понедельник 05:00 утра
            start_of_week = (now - timedelta(days=now.weekday())).replace(hour=5, minute=0, second=0, microsecond=0)
            # Текущее время уже установлено на 05:00 утра сегодняшнего дня
            date_condition = f"master.RequestTime >= '{start_of_week}'"
        elif time_period == 'last_week':
            start_of_last_week = now - timedelta(days=now.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"master.RequestTime >= '{start_of_last_week}' AND master.RequestTime < '{end_of_last_week + timedelta(days=1)}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"master.RequestTime >= '{start_of_month}'"
        else:
            date_condition = "1=1"  # В слquery_get_devices_Yaleучае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL ORDER BY ClientSite, IOSSerialNumber"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Yale_for_last_month(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)

        start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=5, minute=0, second=0,
                                                                               microsecond=0)
        end_of_last_month = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)

        print("Start of Last Month:", start_of_last_month)
        print("End of Last Month:", end_of_last_month)

        date_condition1 = f"master.RequestTime >= '{start_of_last_month}'"
        date_condition2 = f"master.RequestTime < '{end_of_last_month}'"

        # Формирование нового SQL-запроса с использованием ANY_VALUE и суммированием
        query = f"""
        SELECT
          ANY_VALUE(ClientSite) AS ClientSite,
          ANY_VALUE(IOSSerialNumber) AS IOSSerialNumber,
          SUM(TotalTransactions) AS TotalTransactions,
          SUM(ServiceMinutes) AS ServiceMinutes
        FROM (
          (
            SELECT
              CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite,
              q2.PropertyValue AS IOSSerialNumber,
              COUNT(*) AS TotalTransactions,
              SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes
            FROM voyce.serviceitemmaster_historic AS master
            INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId
            LEFT JOIN voyce.YClientInfoNM2 c ON (
              master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')
            )
            LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId
              AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != ''
            WHERE {date_condition1} and req.RequestStatusCodeId NOT IN (1, 2) and master.ServiceItemStatusCodeId != 3
              AND master.RequestCompanyId = 1899
            GROUP BY ClientSite, IOSSerialNumber
            HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL
          )
          UNION ALL
          (
            SELECT
              CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite,
              q2.PropertyValue AS IOSSerialNumber,
              COUNT(*) AS TotalTransactions,
              SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes
            FROM voyce.serviceitemmaster AS master
            INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request AS req ON child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId
            LEFT JOIN voyce.YClientInfoNM2 c ON (
              master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')
            )
            LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId
              AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != ''
            WHERE {date_condition2} and req.RequestStatusCodeId NOT IN (1, 2) and master.ServiceItemStatusCodeId != 3
              AND master.RequestCompanyId = 1899
            GROUP BY ClientSite, IOSSerialNumber
            HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL
          )
        ) AS subquery
        GROUP BY IOSSerialNumber
        ORDER BY ClientSite, IOSSerialNumber;
        """

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_NM_for_last_month(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)

        start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=5, minute=0, second=0,
                                                                               microsecond=0)
        end_of_last_month = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)

        print("Start of Last Month:", start_of_last_month)
        print("End of Last Month:", end_of_last_month)

        date_condition1 = f"master.RequestTime >= '{start_of_last_month}'"
        date_condition2 = f"master.RequestTime < '{end_of_last_month}'"

        query = f"""
        SELECT
          ANY_VALUE(ClientSite) AS ClientSite,
          ANY_VALUE(IOSSerialNumber) AS IOSSerialNumber,
          SUM(TotalTransactions) AS TotalTransactions,
          SUM(ServiceMinutes) AS ServiceMinutes
        FROM (
          (
            SELECT
              CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite,
              q2.PropertyValue AS IOSSerialNumber,
              COUNT(*) AS TotalTransactions,
              SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes
            FROM voyce.serviceitemmaster_historic AS master
            INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId
            LEFT JOIN voyce.YClientInfoNM2 c ON (
              master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')
            )
            LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId
              AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != ''
            WHERE {date_condition1} and req.RequestStatusCodeId NOT IN (1, 2) and master.ServiceItemStatusCodeId != 3
              AND master.RequestCompanyId = 1598
            GROUP BY ClientSite, IOSSerialNumber
            HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL
          )
          UNION ALL
          (
            SELECT
              CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite,
              q2.PropertyValue AS IOSSerialNumber,
              COUNT(*) AS TotalTransactions,
              SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes
            FROM voyce.serviceitemmaster AS master
            INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId
            INNER JOIN voyce.request AS req ON child.RequestId = req.Id
            LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId
            LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
            LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId
            LEFT JOIN voyce.YClientInfoNM2 c ON (
              master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')
            )
            LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId
              AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != ''
            WHERE {date_condition2} and req.RequestStatusCodeId NOT IN (1, 2) and master.ServiceItemStatusCodeId != 3
              AND master.RequestCompanyId = 1598
            GROUP BY ClientSite, IOSSerialNumber
            HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL
          )
        ) AS subquery
        GROUP BY IOSSerialNumber
        ORDER BY ClientSite, IOSSerialNumber;
        """

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_NM_for_last_30_days(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра
        start_date = now - timedelta(days=30)  # Вычисляем дату 30 дней назад

        print("Start of Last 30 Days:", start_date)
        print("End of Last 30 Days:", now)

        date_condition = f"master.RequestTime >= '{start_date.strftime('%Y-%m-%d %H:%M:%S')}'"
        # Формирование SQL-запроса с использованием date_condition
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL UNION ALL SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL ORDER BY ClientSite, IOSSerialNumber;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                # print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Yale_for_last_30_days(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)  # Устанавливаем время на 05:00 утра
        start_date = now - timedelta(days=30)  # Вычисляем дату 30 дней назад

        print("Start of Last 30 Days:", start_date)
        print("End of Last 30 Days:", now)

        date_condition = f"master.RequestTime >= '{start_date.strftime('%Y-%m-%d %H:%M:%S')}'"
        # Формирование SQL-запроса с использованием date_condition
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL UNION ALL SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL ORDER BY ClientSite, IOSSerialNumber;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                # print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_NM_this_year(self):
        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)

        start_of_year = now.replace(month=1, day=1)
        formatted_start_of_year = start_of_year.strftime('%Y-%m-%d %H:%M:%S')

        date_condition = f"master.RequestTime >= '{formatted_start_of_year}'"
        print(formatted_start_of_year)
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue HAVING ClientSite is not null and IOSSerialNumber is NOT NULL UNION ALL SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL ORDER BY ClientSite, IOSSerialNumber;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Yale_this_year(self):
        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)

        start_of_year = now.replace(month=1, day=1)
        formatted_start_of_year = start_of_year.strftime('%Y-%m-%d %H:%M:%S')

        date_condition = f"master.RequestTime >= '{formatted_start_of_year}'"
        print(formatted_start_of_year)
        query = f"SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue HAVING ClientSite is not null and IOSSerialNumber is NOT NULL UNION ALL SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition} AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue HAVING ClientSite IS NOT NULL AND IOSSerialNumber IS NOT NULL ORDER BY ClientSite, IOSSerialNumber;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_Yale_last_year(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=6, minute=0, second=0,
                                     microsecond=0)  # Сейчас, но установлено время на 05:00 утра
        start_of_last_year = (now.replace(month=1, day=1, year=now.year - 1))  # Начало прошлого года
        end_of_this_year = now.replace(month=1, day=1)  # Начало текущего года

        # Форматирование дат для SQL-запроса
        formatted_start_of_last_year = start_of_last_year.strftime('%Y-%m-%d %H:%M:%S')
        formatted_end_of_this_year = end_of_this_year.strftime('%Y-%m-%d %H:%M:%S')

        # Условие для запроса первой части, использующее начало и конец последнего года
        date_condition1 = f"master.RequestTime >= '{formatted_start_of_last_year}' and master.RequestTime <= '{formatted_end_of_this_year}'"
        # Условие для запроса второй части, использующее конец текущего года
        date_condition2 = f"master.RequestTime <= '{formatted_end_of_this_year}' and master.RequestTime <= '{formatted_end_of_this_year}'"
        print(start_of_last_year)
        print(end_of_this_year)

        # Формирование SQL-запроса
        query = f"SELECT * FROM ((SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition1} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL ) UNION ALL (SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition2} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1899 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL )) ORDER BY ClientSite, IOSSerialNumber"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                # print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_get_devices_NM_last_year(self):
        print("Starting to execute the query...")

        now = datetime.now().replace(hour=6, minute=0, second=0,
                                     microsecond=0)  # Сейчас, но установлено время на 05:00 утра
        start_of_last_year = (now.replace(month=1, day=1, year=now.year - 1))  # Начало прошлого года
        end_of_this_year = now.replace(month=1, day=1)  # Начало текущего года

        # Форматирование дат для SQL-запроса
        formatted_start_of_last_year = start_of_last_year.strftime('%Y-%m-%d %H:%M:%S')
        formatted_end_of_this_year = end_of_this_year.strftime('%Y-%m-%d %H:%M:%S')

        # Условие для запроса первой части, использующее начало и конец последнего года
        date_condition1 = f"master.RequestTime >= '{formatted_start_of_last_year}' and master.RequestTime <= '{formatted_end_of_this_year}'"
        # Условие для запроса второй части, использующее конец текущего года
        date_condition2 = f"master.RequestTime <= '{formatted_end_of_this_year}' and master.RequestTime <= '{formatted_end_of_this_year}'"
        print(start_of_last_year)
        print(end_of_this_year)

        # Формирование SQL-запроса
        query = f"SELECT * FROM ((SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster_historic AS master INNER JOIN voyce.serviceitemdetail_historic AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request_historic as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession_historic AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput_historic AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition1} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL ) UNION ALL (SELECT CASE WHEN i.DataInputValue IS NOT NULL THEN i.DataInputValue ELSE c.Site END AS ClientSite, q2.PropertyValue AS IOSSerialNumber, COUNT(*) AS TotalTransactions, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId LEFT JOIN voyce.AppUser AS app ON app.UserType = 'ClientUser' AND app.SourceId = master.ClientUserId LEFT JOIN voyce.YClientInfoNM2 c ON (master.ClientUserId = c.ClientUserId OR app.LoginName = CONCAT(c.SerialNumber, '@NM.weyivideo.com')) LEFT JOIN voyce.serviceitemdatainput AS i ON child.Id = i.ServiceItemDetailId AND i.DataInputName ILIKE 'site' AND i.DataInputValue IS NOT NULL AND i.DataInputValue != '' WHERE {date_condition2} and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1598 GROUP BY ClientSite, q2.PropertyValue, i.DataInputValue having ClientSite is not null and IOSSerialNumber is NOT NULL )) ORDER BY ClientSite, IOSSerialNumber"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                aggregated_data = defaultdict(lambda: {'TotalTransactions': 0, 'ServiceMinutes': 0})

                for row in rows:
                    key = (row['ClientSite'], row['IOSSerialNumber'])
                    aggregated_data[key]['TotalTransactions'] += row['TotalTransactions']
                    aggregated_data[key]['ServiceMinutes'] += row['ServiceMinutes']

                aggregated_rows = [Row(ClientSite=key[0], IOSSerialNumber=key[1], **values) for key, values in
                                   aggregated_data.items()]
                # print(aggregated_rows)
                return aggregated_rows

        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_interpreter_dashboard(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        print(now)
        query = f"""
        WITH TargetLanguages AS (
            SELECT 
            p.Id AS InterpreterId,
            array_distinct(collect_list(lang.EnglishName)) AS UniqueTargetLanguages
            FROM voyce.provider AS p
            LEFT JOIN voyce.requestprovider AS rp ON p.Id = rp.ProviderId
            LEFT JOIN voyce.serviceitemdetail AS child ON child.RequestId = rp.RequestId
            INNER JOIN voyce.request AS req ON child.RequestId = req.Id
            INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
            LEFT JOIN voyce.serviceitemmaster AS master ON master.id = child.ServiceItemMasterId
            LEFT JOIN voyce.billcompanyproduct AS cp ON cp.Id = master.RequestBillCompanyProductId
            where 
              master.RequestTime >= '{now}'
              AND lang.EnglishName not ilike '%operator%'
            GROUP BY p.id
        )
        select egged.*,
        txn.RequestId as RequestId,
        c.CompanyCode as CompanyCode,
        c.Id as InterpreterCompanyId,
        case
        when txn.RequestId is not null then 'In conference'
        when pos.ProviderOnlineStatusCodeId = 1 then 'online'
        else 'offline'
        end as Status,
        pos.OffLineReasonDetail
        from  (SELECT p.Id AS InterpreterId,
        any_value(p.Name) as InterpreterName,
        TargetLanguages.UniqueTargetLanguages AS UniqueTargetLanguages,
        any_value(master.RequestCompanyId) AS CompanyId,
        any_value(master.ClientId) AS ClientId,
        COUNT(*) AS TotalCalls,
        SUM(
        unix_timestamp(rp.AcceptedTime) - unix_timestamp(rp.ReceivedTime)
        ) AS TotalWaitTime,
        SUM(
        CASE
        WHEN rp.AcceptedTime IS NOT NULL THEN 1
        ELSE 0
        END
        ) AS TotalCallsAccepted,
        SUM(
        CASE
        WHEN rp.ConfirmedTime IS NOT NULL THEN 1
        ELSE 0
        END
        ) AS TotalCallsAnswered,
        SUM(
        CASE
        WHEN rp.ReceivedTime IS NOT NULL
        AND rp.AcceptedTime IS NULL THEN 1
        ELSE 0
        END
        ) AS TotalCallsMissed,
        SUM(
        CEIL(
        CASE
        WHEN child.ProviderId = p.id THEN child.ServiceSeconds / 60
        ELSE 0
        END
        )
        ) AS TotalServiceMinutes from
        voyce.provider as p
        left join voyce.requestprovider as rp on p.Id = rp.ProviderId
        left join voyce.serviceitemdetail as child on child.RequestId = rp.RequestId
        left JOIN voyce.request as req on child.RequestId = req.Id
        left join voyce.language as lang on lang.Id = child.TargetLanguageId
        left join voyce.serviceitemmaster as master on master.id = child.ServiceItemMasterId
        left join voyce.billcompanyproduct as cp on cp.Id = master.RequestBillCompanyProductId
        LEFT JOIN TargetLanguages AS TargetLanguages ON p.Id = TargetLanguages.InterpreterId
        where master.RequestTime >= '{now}'
        and req.RequestStatusCodeId not in (1, 2)
        and master.ServiceItemStatusCodeId != 3
        and lang.EnglishName not ilike '%operator%'
        and p.Name not ilike '%test%'
        and p.LastName not ilike '%test%'
        and p.Available = true
        GROUP BY
        p.id,
        TargetLanguages.UniqueTargetLanguages) as egged
        left join voyce.lspprovider as lsp on egged.InterpreterId = lsp.ProviderId
        left join voyce.company as c on lsp.CompanyId = c.Id
        LEFT JOIN (
        select
        child.RequestId,
        child.ProviderId,
        master.ClientId,
        master.RequestCompanyId
        from
        voyce.serviceitemdetail as child
        inner join voyce.request as req on child.RequestId = req.Id
        inner join voyce.serviceitemmaster as master on master.Id = child.ServiceItemMasterId
        where
        req.RequestStatusCodeId in (1,2)
        ) as txn on txn.ProviderId = egged.InterpreterId
        LEFT JOIN (
        SELECT
        pos.*,
        ROW_NUMBER() OVER (PARTITION BY pos.ProviderId ORDER BY pos.LastUpdate DESC) AS rn
        FROM voyce.provideronlinestatus AS pos
        ) AS pos ON pos.ProviderId = egged.InterpreterId AND pos.rn = 1
        LEFT JOIN voyce.codelist as cd on cd.Category = 'ProviderOffReason' and cd.CodeId = pos.OffLineReasonCodeId
        where
        c.id = 1604
        """
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    print(row)
                return result
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None

    def query_interpreter_dashboard_periods(self, time_period):
        print("Starting to execute the query...")

        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Устанавливаем время на 06:00 утра

        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday = now - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{yesterday.strftime('%Y-%m-%d')}' and master.RequestTime < '{now}'"
        elif time_period == 'this_week':
            start_of_week = (now - timedelta(days=now.weekday())).replace(hour=6, minute=0, second=0, microsecond=0)
            date_condition = f"master.RequestTime >= '{start_of_week.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_week':
            start_of_last_week = (now - timedelta(days=now.weekday() + 7)).replace(hour=6, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_week = start_of_last_week + timedelta(days=7)
            date_condition = f"master.RequestTime >= '{start_of_last_week.strftime('%Y-%m-%d')}' AND master.RequestTime < '{end_of_last_week.strftime('%Y-%m-%d')}'"
            print(start_of_last_week)
            print(end_of_last_week)
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"master.RequestTime >= '{start_of_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_30_days':
            thirty_days_ago = now - timedelta(days=30)
            date_condition = f"master.RequestTime >= '{thirty_days_ago.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_month':
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=6, minute=0, second=0,
                                                                                   microsecond=0)
            end_of_last_month = now.replace(day=1, hour=6, minute=0, second=0, microsecond=0)
            date_condition = f"master.RequestTime >= '{start_of_last_month.strftime('%Y-%m-%d')}' AND master.RequestTime < '{end_of_last_month.strftime('%Y-%m-%d')}'"
            print(start_of_last_month)
            print(end_of_last_month)
        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1)
            date_condition = f"master.RequestTime >= '{start_of_year.strftime('%Y-%m-%d')}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"""
            WITH TargetLanguagesHistoric AS (
                SELECT
                p.Id AS InterpreterId,
                array_distinct(collect_list(lang.EnglishName)) AS UniqueTargetLanguages
                FROM voyce.provider AS p
                LEFT JOIN voyce.requestprovider_historic AS rp ON p.Id = rp.ProviderId
                LEFT JOIN voyce.serviceitemdetail_historic AS child ON child.RequestId = rp.RequestId
                INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id
                INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
                LEFT JOIN voyce.serviceitemmaster_historic AS master ON master.id = child.ServiceItemMasterId
                LEFT JOIN voyce.billcompanyproduct AS cp ON cp.Id = master.RequestBillCompanyProductId
                WHERE {date_condition}
                  AND lang.EnglishName NOT ILIKE '%operator%'
                GROUP BY p.id
            ),
            TargetLanguages AS (
                SELECT 
                p.Id AS InterpreterId,
                array_distinct(collect_list(lang.EnglishName)) AS UniqueTargetLanguages
                FROM voyce.provider AS p
                LEFT JOIN voyce.requestprovider AS rp ON p.Id = rp.ProviderId
                LEFT JOIN voyce.serviceitemdetail AS child ON child.RequestId = rp.RequestId
                INNER JOIN voyce.request AS req ON child.RequestId = req.Id
                INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
                LEFT JOIN voyce.serviceitemmaster AS master ON master.id = child.ServiceItemMasterId
                LEFT JOIN voyce.billcompanyproduct AS cp ON cp.Id = master.RequestBillCompanyProductId
                WHERE {date_condition}
                  AND lang.EnglishName NOT ILIKE '%operator%'
                GROUP BY p.id
            )
            SELECT egged.*,
                  txn.RequestId AS RequestId,
                  c.CompanyCode AS CompanyCode,
                  c.Id AS InterpreterCompanyId,
                  CASE
                      WHEN txn.RequestId IS NOT NULL THEN 'In conference'
                      WHEN pos.ProviderOnlineStatusCodeId = 1 THEN 'online'
                      ELSE 'offline'
                  END AS Status,
                  pos.OffLineReasonDetail
            FROM (
                SELECT 
                p.Id AS InterpreterId,
                any_value(p.Name) AS InterpreterName,
                TargetLanguagesHistoric.UniqueTargetLanguages AS UniqueTargetLanguages,
                any_value(master.RequestCompanyId) AS CompanyId,
                any_value(master.ClientId) AS ClientId,
                COUNT(*) AS TotalCalls,
                SUM(
                    unix_timestamp(rp.AcceptedTime) - unix_timestamp(rp.ReceivedTime)
                ) AS TotalWaitTime,
                SUM(
                    CASE
                        WHEN rp.AcceptedTime IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS TotalCallsAccepted,
                SUM(
                    CASE
                        WHEN rp.ConfirmedTime IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS TotalCallsAnswered,
                SUM(
                    CASE
                        WHEN rp.ReceivedTime IS NOT NULL
                        AND rp.AcceptedTime IS NULL THEN 1
                        ELSE 0
                    END
                ) AS TotalCallsMissed,
                SUM(
                    CEIL(
                        CASE
                            WHEN child.ProviderId = p.id THEN child.ServiceSeconds / 60
                            ELSE 0
                        END
                    )
                ) AS TotalServiceMinutes
                FROM voyce.provider AS p
                LEFT JOIN voyce.requestprovider_historic AS rp ON p.Id = rp.ProviderId
                LEFT JOIN voyce.serviceitemdetail_historic AS child ON child.RequestId = rp.RequestId
                LEFT JOIN voyce.request_historic AS req ON child.RequestId = req.Id
                LEFT JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
                LEFT JOIN voyce.serviceitemmaster_historic AS master ON master.id = child.ServiceItemMasterId
                LEFT JOIN voyce.billcompanyproduct AS cp ON cp.Id = master.RequestBillCompanyProductId
                LEFT JOIN TargetLanguagesHistoric AS TargetLanguagesHistoric ON p.Id = TargetLanguagesHistoric.InterpreterId
                WHERE {date_condition}
                  AND req.RequestStatusCodeId NOT IN (1, 2)
                  AND master.ServiceItemStatusCodeId != 3
                  AND lang.EnglishName NOT ILIKE '%operator%'
                  AND p.Name NOT ILIKE '%test%'
                  AND p.LastName NOT ILIKE '%test%'
                  AND p.Available = TRUE
                GROUP BY
                  p.id,
                  TargetLanguagesHistoric.UniqueTargetLanguages
                UNION ALL
                SELECT 
                p.Id AS InterpreterId,
                any_value(p.Name) AS InterpreterName,
                TargetLanguages.UniqueTargetLanguages AS UniqueTargetLanguages,
                any_value(master.RequestCompanyId) AS CompanyId,
                any_value(master.ClientId) AS ClientId,
                COUNT(*) AS TotalCalls,
                SUM(
                    unix_timestamp(rp.AcceptedTime) - unix_timestamp(rp.ReceivedTime)
                ) AS TotalWaitTime,
                SUM(
                    CASE
                        WHEN rp.AcceptedTime IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS TotalCallsAccepted,
                SUM(
                    CASE
                        WHEN rp.ConfirmedTime IS NOT NULL THEN 1
                        ELSE 0
                    END
                ) AS TotalCallsAnswered,
                SUM(
                    CASE
                        WHEN rp.ReceivedTime IS NOT NULL
                        AND rp.AcceptedTime IS NULL THEN 1
                        ELSE 0
                    END
                ) AS TotalCallsMissed,
                SUM(
                    CEIL(
                        CASE
                            WHEN child.ProviderId = p.id THEN child.ServiceSeconds / 60
                            ELSE 0
                        END
                    )
                ) AS TotalServiceMinutes
                FROM voyce.provider AS p
                LEFT JOIN voyce.requestprovider AS rp ON p.Id = rp.ProviderId
                LEFT JOIN voyce.serviceitemdetail AS child ON child.RequestId = rp.RequestId
                LEFT JOIN voyce.request AS req ON child.RequestId = req.Id
                LEFT JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
                LEFT JOIN voyce.serviceitemmaster AS master ON master.id = child.ServiceItemMasterId
                LEFT JOIN voyce.billcompanyproduct AS cp ON cp.Id = master.RequestBillCompanyProductId
                LEFT JOIN TargetLanguages AS TargetLanguages ON p.Id = TargetLanguages.InterpreterId
                WHERE {date_condition}
                  AND req.RequestStatusCodeId NOT IN (1, 2)
                  AND master.ServiceItemStatusCodeId != 3
                  AND lang.EnglishName NOT ILIKE '%operator%'
                  AND p.Name NOT ILIKE '%test%'
                  AND p.LastName NOT ILIKE '%test%'
                  AND p.Available = TRUE
                GROUP BY
                  p.id,
                  TargetLanguages.UniqueTargetLanguages
            ) AS egged
            LEFT JOIN voyce.lspprovider AS lsp ON egged.InterpreterId = lsp.ProviderId
            LEFT JOIN voyce.company AS c ON lsp.CompanyId = c.Id
            LEFT JOIN (
                SELECT 
                child.RequestId,
                child.ProviderId,
                master.ClientId,
                master.RequestCompanyId
                FROM voyce.serviceitemdetail AS child
                INNER JOIN voyce.request AS req ON child.RequestId = req.Id
                INNER JOIN voyce.serviceitemmaster AS master ON master.Id = child.ServiceItemMasterId
                WHERE req.RequestStatusCodeId IN (1, 2)
            ) AS txn ON txn.ProviderId = egged.InterpreterId
            LEFT JOIN (
                SELECT 
                pos.*,
                ROW_NUMBER() OVER (PARTITION BY pos.ProviderId ORDER BY pos.LastUpdate DESC) AS rn
                FROM voyce.provideronlinestatus AS pos
            ) AS pos ON pos.ProviderId = egged.InterpreterId AND pos.rn = 1
            LEFT JOIN voyce.codelist AS cd ON cd.Category = 'ProviderOffReason' AND cd.CodeId = pos.OffLineReasonCodeId
            WHERE c.id = 1604;
        """

        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                # Определение имен полей для создания словарей
                columns = [desc[0] for desc in cursor.description]
                result_dicts = [dict(zip(columns, row)) for row in result]

                # Аггрегируем данные
                aggregated_results = {}
                for row in result_dicts:
                    interpreter_id = row['InterpreterId']
                    if interpreter_id not in aggregated_results:
                        aggregated_results[interpreter_id] = row
                    else:
                        aggregated_results[interpreter_id]['TotalCalls'] += row['TotalCalls']
                        aggregated_results[interpreter_id]['TotalWaitTime'] += row['TotalWaitTime']
                        aggregated_results[interpreter_id]['TotalCallsAccepted'] += row['TotalCallsAccepted']
                        aggregated_results[interpreter_id]['TotalCallsAnswered'] += row['TotalCallsAnswered']
                        aggregated_results[interpreter_id]['TotalCallsMissed'] += row['TotalCallsMissed']
                        aggregated_results[interpreter_id]['TotalServiceMinutes'] += row['TotalServiceMinutes']

                # Преобразуем обратно в namedtuple для совместимости с остальным кодом
                InterpreterRow = namedtuple('InterpreterRow', columns)
                final_results = [InterpreterRow(**row) for row in aggregated_results.values()]

                print("Query results:")
                for row in final_results:
                    print(row)  # Вывод каждой строки результата

                return final_results  # Возвращаем результат
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_interpreter_dashboard_periods1(self, time_period):
        print("Starting to execute the query...")

        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)  # Устанавливаем время на 06:00 утра

        # Определение date_condition в зависимости от time_period
        if time_period == 'last_year':
            start_of_last_year = now.replace(year=now.year - 1, month=1, day=1)
            end_of_last_year = now.replace(month=1, day=1) - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{start_of_last_year.strftime('%Y-%m-%d')}' AND master.RequestTime < '{end_of_last_year.strftime('%Y-%m-%d')}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        # Формирование SQL-запроса с учетом date_condition
        query = f"""
                WITH TargetLanguages AS (
                SELECT
                p.Id AS InterpreterId,
                array_distinct(collect_list(lang.EnglishName)) AS UniqueTargetLanguages
                FROM voyce.provider AS p
                LEFT JOIN voyce.requestprovider_historic AS rp ON p.Id = rp.ProviderId
                LEFT JOIN voyce.serviceitemdetail_historic AS child ON child.RequestId = rp.RequestId
                INNER JOIN voyce.request_historic AS req ON child.RequestId = req.Id
                INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
                LEFT JOIN voyce.serviceitemmaster_historic AS master ON master.id = child.ServiceItemMasterId
                LEFT JOIN voyce.billcompanyproduct AS cp ON cp.Id = master.RequestBillCompanyProductId
                where {date_condition}
                  AND lang.EnglishName not ilike "%operator%"
                GROUP BY p.id
                  )
                select egged.*,
              txn.RequestId as RequestId,
              c.CompanyCode as CompanyCode,
              c.Id as InterpreterCompanyId,
              case
              when txn.RequestId is not null then 'In conference'
              when pos.ProviderOnlineStatusCodeId = 1 then 'online'
              else 'offline'
              end as Status,
              pos.OffLineReasonDetail
              from  (SELECT p.Id AS InterpreterId,
                any_value(p.Name) as InterpreterName,
                TargetLanguages.UniqueTargetLanguages AS UniqueTargetLanguages,
                any_value(master.RequestCompanyId) AS CompanyId,
                any_value(master.ClientId) AS ClientId,
                COUNT(*) AS TotalCalls,
                SUM(
                unix_timestamp(rp.AcceptedTime) - unix_timestamp(rp.ReceivedTime)
                ) AS TotalWaitTime,
                SUM(
                CASE
                WHEN rp.AcceptedTime IS NOT NULL THEN 1
                ELSE 0
                END
                ) AS TotalCallsAccepted,
                SUM(
                CASE
                WHEN rp.ConfirmedTime IS NOT NULL THEN 1
                ELSE 0
                END
                ) AS TotalCallsAnswered,
                SUM(
                CASE
                WHEN rp.ReceivedTime IS NOT NULL
                AND rp.AcceptedTime IS NULL THEN 1
                ELSE 0
                END
                ) AS TotalCallsMissed,
                SUM(
                CEIL(
                CASE
                WHEN child.ProviderId = p.id THEN child.ServiceSeconds / 60
                ELSE 0
                END
                )
                ) AS TotalServiceMinutes from voyce.provider as p
              left join voyce.requestprovider_historic as rp on p.Id = rp.ProviderId
              left join voyce.serviceitemdetail_historic as child on child.RequestId = rp.RequestId
              left JOIN voyce.request_historic as req on child.RequestId = req.Id
              left join voyce.language as lang on lang.Id = child.TargetLanguageId
              left join voyce.serviceitemmaster_historic as master on master.id = child.ServiceItemMasterId
              left join voyce.billcompanyproduct as cp on cp.Id = master.RequestBillCompanyProductId
              LEFT JOIN TargetLanguages AS TargetLanguages ON p.Id = TargetLanguages.InterpreterId
              where {date_condition}
              and req.RequestStatusCodeId not in (1, 2)
              and master.ServiceItemStatusCodeId != 3
              and lang.EnglishName not ilike "%operator%"
              and p.Name not ilike '%test%'
              and p.LastName not ilike '%test%'
              and p.Available = true
              GROUP BY
              p.id,
              TargetLanguages.UniqueTargetLanguages) as egged
              left join voyce.lspprovider as lsp on egged.InterpreterId = lsp.ProviderId
              left join voyce.company as c on lsp.CompanyId = c.Id
              LEFT JOIN (
              select
              child.RequestId,
              child.ProviderId,
              master.ClientId,
              master.RequestCompanyId
              from
              voyce.serviceitemdetail as child
              inner join voyce.request as req on child.RequestId = req.Id
              inner join voyce.serviceitemmaster as master on master.Id = child.ServiceItemMasterId
              where
              req.RequestStatusCodeId in (1,2)
              ) as txn on txn.ProviderId = egged.InterpreterId
              LEFT JOIN (
              SELECT
              pos.*,
              ROW_NUMBER() OVER (PARTITION BY pos.ProviderId ORDER BY pos.LastUpdate DESC) AS rn
              FROM voyce.provideronlinestatus AS pos
              ) AS pos ON pos.ProviderId = egged.InterpreterId AND pos.rn = 1
              LEFT JOIN voyce.codelist as cd on cd.Category = 'ProviderOffReason' and cd.CodeId = pos.OffLineReasonCodeId
              where
              c.id = 1604;"""

        try:
            print("Trying to fetch data...")
            # Здесь должен быть код для выполнения запроса к базе данных
            # Предполагаем, что это что-то вроде:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result  # Возвращаем результат
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_check_QA_HUD(self, time_period):
        print("Starting to execute the query for the time period:", time_period)

        now = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)

        if time_period == 'this_month':
            # Вычесть 45 дней от текущей даты для текущего месяца
            date_45_days_ago = now - timedelta(days=45)
            date_condition = f"main.CreateDate >= '{date_45_days_ago.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_month':
            # Первый день текущего месяца
            start_current_month = now.replace(day=1)
            # Первый день прошлого месяца минус 45 дней
            start = (start_current_month - timedelta(days=45)).replace(hour=0, minute=0, second=0, microsecond=0)
            # Последний день прошлого месяца
            end = start_current_month - timedelta(seconds=1)
            date_condition = f"main.CreateDate >= '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND main.CreateDate <= '{end.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            raise ValueError("Invalid time period specified.")

        query = f"select main.Id as InterpreterId, any_value(main.Name) as FirstName, any_value(main.LastName) as LastName, CONCAT(any_value(main.Name), ' ', any_value(main.LastName)) as InterpreterName, any_value(main.CreateDate) as InterpreterJoinDate, any_value(c.CompanyCode) as CompanyCode, any_value(c.Id) as CompanyId, case when any_value(txn.RequestId) is not null then 'In conference' when any_value(pos.ProviderOnlineStatusCodeId) = 1 then 'Online' else 'Offline' end as Status, any_value(txn.RequestId) as RequestId, array_distinct(array_union(collect_set(lang1.EnglishName), collect_set(lang2.EnglishName))) as Languages from voyce.provider as main left join ( select ProviderId, Deleted, Active, LanguageId1, LanguageId2 from voyce.providerservice UNION ALL select ProviderId, Deleted, Active, LanguageId1, LanguageId2 from voyce.providerservice_historic ) as service on main.Id = service.ProviderId left join voyce.Language as lang1 on service.LanguageId1 = lang1.Id left join voyce.Language as lang2 on service.LanguageId2 = lang2.Id left join voyce.lspprovider as lsp on main.Id = lsp.ProviderId left join voyce.company as c on lsp.CompanyId = c.Id left join voyce.activitymonitorv2 as txn on txn.ProviderId = main.Id and txn.Status in ('New', 'In Servicef') left join ( SELECT pos.*, ROW_NUMBER() OVER ( PARTITION BY pos.ProviderId ORDER BY pos.LastUpdate DESC ) AS rn FROM voyce.provideronlinestatus AS pos ) AS pos ON pos.ProviderId = main.Id AND pos.rn = 1 where main.Available = true and service.Deleted = false and service.Active = true and main.Name not ilike '%test%' and main.LastName not ilike '%test%' and c.Id in (1265, 1058, 1679, 1404, 1053, 1398, 1264, 1032, 1601, 1033, 1080, 1846) and {date_condition} group by main.Id;"
        try:
            print("Trying to fetch data...")
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                transaction_id_count = len(result)
                self.transaction_id_count = transaction_id_count
                print(f"Total number of ReferenceTransactionId: {self.transaction_id_count}")

                with open('query_results_ADMIN.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])
                    writer.writerows(result)

                return result

        except Exception as e:
            print("An error occurred during query execution:", e)
            return None

    def query_top_languages(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)
        query = f"SELECT a.TargetLanguage, sum(a.ServiceMinutes) as ServiceMinutes, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.CountPendingAudioCalls) as CountPendingAudioCalls, sum(a.CountPendingVideoCalls) as CountPendingVideoCalls, sum(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, sum(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, sum(a.CountNewAudioCalls) as CountNewAudioCalls, sum(a.CountNewVideoCalls) as CountNewVideoCalls, sum(a.CountBackupCalls) as CountBackupCalls, sum(a.BackupWaitingSeconds) as BackupWaitingSeconds, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls FROM voyce.aggbyclienthour as a WHERE a.CompanyId = 1355 and a.DateTime >= '{now}' GROUP by a.TargetLanguage order by ServiceMinutes Desc limit 5;"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_languages_by_hour_11am(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = now + timedelta(days=1)
        query = f"select subquery.TargetLanguage as languageName, sum(subquery.TotalCalls) as TotalCalls, COLLECT_LIST(STRUCT(subquery.thour as hour, subquery.TotalCalls as TotalCalls, subquery.ServiceMinutes as ServiceMinutes, subquery.CountAudioMinute as CountAudioMinute, subquery.CountVideoMinute as CountVideoMinute, subquery.WaitingSeconds as WaitingSeconds, subquery.CountSuccessAudioCalls as CountSuccessAudioCalls, subquery.CountSuccessVideoCalls as CountSuccessVideoCalls, subquery.CountFailedAudioCalls as CountFailedAudioCalls, subquery.CountFailedVideoCalls as CountFailedVideoCalls, subquery.CallQualityRatingStar as CallQualityRatingStar, subquery.CountRatingStarCalls as CountRatingStarCalls)) AS hours from (select TargetLanguage, hour(from_utc_timestamp(CONCAT(`Date`, ' ', `Hour`, ':00:00'), 'America/New_York')) AS tHour, sum(a.ServiceMinutes) as ServiceMinutes, sum(a.CountAudioMinute) as CountAudioMinute, sum(a.CountVideoMinute) as CountVideoMinute, sum(a.WaitingSeconds) as WaitingSeconds, sum(a.TotalCalls) as TotalCalls, sum(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, sum(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, sum(a.CountFailedAudioCalls) as CountFailedAudioCalls, sum(a.CountFailedVideoCalls) as CountFailedVideoCalls, sum(a.CallQualityRatingStar) as CallQualityRatingStar, sum(a.CountRatingStarCalls) as CountRatingStarCalls from voyce.aggbyclienthourtype as a where a.Date >= '{now}' AND a.Date <= '{tomorrow}' and a.TargetLanguage not ilike '%Operator%' and a.ClientId in (44345) and a.CompanyId = 1355 group by tHour, TargetLanguage) as subquery group by subquery.TargetLanguage order by TotalCalls desc"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_languages_by_hour_periods(self, time_period):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Обнуляем время для корректного сравнения дат

        # Определение date_condition в зависимости от time_period
        date_condition = ""
        if time_period == 'yesterday':
            yesterday = now - timedelta(days=1)
            date_condition = f"AND a.Date >= '{yesterday.strftime('%Y-%m-%d')}' AND a.Date < '{now.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_week':
            start_of_week = (now - timedelta(days=now.weekday()))
            date_condition = f"AND a.Date >= '{start_of_week.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_week':
            start_of_last_week = (now - timedelta(days=now.weekday() + 7))
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"AND a.Date >= '{start_of_last_week.strftime('%Y-%m-%d')}' AND a.Date <= '{end_of_last_week.strftime('%Y-%m-%d')}'"
            print(start_of_last_week)
            print(end_of_last_week)
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"AND a.Date >= '{start_of_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_30_days':
            thirty_days_ago = now - timedelta(days=30)
            date_condition = f"AND a.Date >= '{thirty_days_ago.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_month':
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
            end_of_last_month = now.replace(day=1)
            print(start_of_last_month)
            print(end_of_last_month)
            date_condition = f"AND a.Date >= '{start_of_last_month.strftime('%Y-%m-%d')}' AND a.Date < '{end_of_last_month.strftime('%Y-%m-%d')}'"
        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1)
            date_condition = f"AND a.Date >= '{start_of_year.strftime('%Y-%m-%d')}'"
        elif time_period == 'last_year':
            start_of_last_year = now.replace(year=now.year - 1, month=1, day=1)
            end_of_last_year = start_of_last_year + timedelta(days=364)  # Високосный год не учитывается
            date_condition = f"AND a.Date >= '{start_of_last_year.strftime('%Y-%m-%d')}' AND a.Date < '{end_of_last_year.strftime('%Y-%m-%d')}'"

        query = f"""
        SELECT subquery.TargetLanguage as languageName, 
               SUM(subquery.TotalCalls) as TotalCalls, 
               COLLECT_LIST(STRUCT(subquery.thour as hour, 
                                   subquery.TotalCalls as TotalCalls, 
                                   subquery.ServiceMinutes as ServiceMinutes, 
                                   subquery.CountAudioMinute as CountAudioMinute, 
                                   subquery.CountVideoMinute as CountVideoMinute, 
                                   subquery.WaitingSeconds as WaitingSeconds, 
                                   subquery.CountSuccessAudioCalls as CountSuccessAudioCalls, 
                                   subquery.CountSuccessVideoCalls as CountSuccessVideoCalls, 
                                   subquery.CountFailedAudioCalls as CountFailedAudioCalls, 
                                   subquery.CountFailedVideoCalls as CountFailedVideoCalls, 
                                   subquery.CallQualityRatingStar as CallQualityRatingStar, 
                                   subquery.CountRatingStarCalls as CountRatingStarCalls)) AS hours 
        FROM (
            SELECT TargetLanguage, 
                   HOUR(from_utc_timestamp(CONCAT(`Date`, ' ', `Hour`, ':00:00'), 'America/New_York')) AS tHour, 
                   SUM(a.ServiceMinutes) as ServiceMinutes, 
                   SUM(a.CountAudioMinute) as CountAudioMinute, 
                   SUM(a.CountVideoMinute) as CountVideoMinute, 
                   SUM(a.WaitingSeconds) as WaitingSeconds, 
                   SUM(a.TotalCalls) as TotalCalls, 
                   SUM(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, 
                   SUM(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, 
                   SUM(a.CountFailedAudioCalls) as CountFailedAudioCalls, 
                   SUM(a.CountFailedVideoCalls) as CountFailedVideoCalls, 
                   SUM(a.CallQualityRatingStar) as CallQualityRatingStar, 
                   SUM(a.CountRatingStarCalls) as CountRatingStarCalls 
            FROM voyce.aggbyclienthourtype as a 
            WHERE a.ClientId in (44345) AND a.CompanyId = 1355 {date_condition} AND a.TargetLanguage not ilike '%Operator%'
            GROUP BY tHour, TargetLanguage
        ) as subquery 
        GROUP BY subquery.TargetLanguage 
        ORDER BY TotalCalls DESC 
        limit 10
        """

        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def count_total_calls_at_11(self, result):
        self.total_calls_at_11 = 0  # Обнуляем счётчик перед подсчётом
        for row in result:
            if row.languageName == 'Spanish':  # Проверяем, что язык испанский
                for hour_data in row.hours:
                    if hour_data['hour'] == 11:
                        self.total_calls_at_11 += hour_data['TotalCalls']
        print(f"Total Calls at 11:00 for Spanish: {self.total_calls_at_11}")

    def query_active_widget(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"SELECT ANY_VALUE(master.RequestId) AS referencetransactionid, q2.PropertyValue AS IOSSerialNumber, ANY_VALUE(master.RequestTime) AS RequestTime, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes, ANY_VALUE(master.ClientId) as ClientId, ANY_VALUE(master.RequestCompanyId) as CompanyId, COUNT(*) AS NumberOfServices FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE NOT ISNULL(q2.PropertyValue) AND NOT ISNULL(master.RequestId) AND NOT ISNULL(master.RequestTime) AND NOT ISNULL(master.ClientId) AND NOT ISNULL(master.RequestCompanyId) AND master.RequestTime >= '{now1}' AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1673 GROUP BY q2.PropertyValue HAVING IOSSerialNumber is not null"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_all_data_widjets(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where master.RequestTime >= '{now1}' and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1673 order by master.RequestTime desc"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                total_price_sum = 0
                total_waiting_seconds_spanish_audio = 0
                spanish_audio_video_calls_count = 0
                total_waiting_seconds_other_languages_video = 0
                other_languages_video_calls_count = 0

                # Инициализация переменных статусов
                pending = 0
                new = 0
                in_service = 0
                serviced = 0
                cancelled = 0

                for row in result:
                    if 'TotalPrice' in row and row['TotalPrice'] is not None:
                        total_price_sum += row['TotalPrice']
                    total_price_sum = round(total_price_sum, 2)

                    if row['TargetLanguage'] == 'Spanish' and row['VideoOption'] == 'Video' and row[
                        'Status'] == 'Serviced':
                        total_waiting_seconds_spanish_audio += row['WaitingSeconds'] or 0
                        spanish_audio_video_calls_count += 1

                    if row['VideoOption'] == 'Video' and row['Status'] == 'Serviced' and row['TargetLanguage'] not in [
                        'Spanish']:
                        total_waiting_seconds_other_languages_video += row['WaitingSeconds'] or 0
                        other_languages_video_calls_count += 1

                    # Подсчет статусов
                    if row['Status'] == 'Pending':
                        pending += 1
                    elif row['Status'] == 'New':
                        new += 1
                    elif row['Status'] == 'In Service':
                        in_service += 1
                    elif row['Status'] == 'Serviced':
                        serviced += 1
                    elif row['Status'] == 'Cancelled':
                        cancelled += 1

                total_calls_serviced = cancelled + serviced
                minutes_used = sum(row['ServiceMinutes'] or 0 for row in result)
                completed_audio_calls = serviced - spanish_audio_video_calls_count - other_languages_video_calls_count

                if spanish_audio_video_calls_count > 0:
                    average_waiting_time_per_spanish_video_call = round(
                        total_waiting_seconds_spanish_audio / spanish_audio_video_calls_count)
                else:
                    average_waiting_time_per_spanish_video_call = 0

                if other_languages_video_calls_count > 0:
                    avg_waiting_seconds_video_ol = round(
                        total_waiting_seconds_other_languages_video / other_languages_video_calls_count)
                else:
                    avg_waiting_seconds_video_ol = 0

                if total_calls_serviced > 0:
                    avg_call_length_mins = round(minutes_used / total_calls_serviced)
                else:
                    avg_call_length_mins = 0

                # Вывод общей информации
                print(f"Total Price Sum: {total_price_sum}")
                print(f"Average Waiting Time per Spanish Video Call: {average_waiting_time_per_spanish_video_call}")
                print(f"AVG Wait Seconds Video (Other Languages): {avg_waiting_seconds_video_ol}")
                print(
                    f"Pending: {pending}, New: {new}, In Service: {in_service}, Serviced: {serviced}, Cancelled: {cancelled}")
                print(f"Total Calls Serviced (Cancelled + Serviced): {total_calls_serviced}")
                print(f"Completed Video Calls: {spanish_audio_video_calls_count + other_languages_video_calls_count}")
                print(f"Completed Audio Calls: {completed_audio_calls}")
                print(f"Minutes Used: {minutes_used}")
                print(f"Avg Call Length Mins: {avg_call_length_mins}")

                return total_price_sum, other_languages_video_calls_count, spanish_audio_video_calls_count, pending, new, in_service, serviced, cancelled, total_calls_serviced, completed_audio_calls, minutes_used, average_waiting_time_per_spanish_video_call, avg_waiting_seconds_video_ol, avg_call_length_mins
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    def query_all_data_widjets_Admin(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        now2 = '2024-08-28 00:00:00'
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"""
            SELECT 
                HOUR(FROM_UTC_TIMESTAMP(child.RequestTime, 'America/New_York')) AS Hour,
                master.RequestTime AS RequestTime,
                child.RequestId AS RequestId,
                master.RequestCompanyId AS CompanyId,
                master.ClientId AS ClientId,
                lang.EnglishName AS Language,
                lang.Id AS LanguageId,
                master.IsVideo AS IsVideo,
                CEIL((child.ServiceSeconds)/60) AS ServiceMinutes,
                child.WaitSeconds AS WaitSeconds,
                eva.Answer AS Rating,
                CEIL(rp.TotalPrice) AS TotalPrice,
                CASE WHEN eva.Answer IS NOT NULL THEN 1 ELSE 0 END AS RatedCalls,
                CASE master.IsVideo WHEN true THEN 'Video' ELSE 'Audio' END AS CallType,
                CASE master.IsVideo WHEN true THEN CEIL((child.ServiceSeconds)/60) ELSE 0 END AS VideoMinutes,
                CASE master.IsVideo WHEN false THEN CEIL((child.ServiceSeconds)/60) ELSE 0 END AS AudioMinutes,
                CASE master.IsVideo WHEN true THEN 1 ELSE 0 END AS VideoCall,
                CASE master.IsVideo WHEN false THEN 1 ELSE 0 END AS AudioCall,
                CASE master.RoutedToBackup WHEN true THEN 1 ELSE 0 END AS BackupCall,
                CASE WHEN lang.Id = 44 THEN 1 ELSE 0 END AS SpanishCall,
                CASE WHEN lang.Id = 44 THEN child.WaitSeconds ELSE 0 END AS SpanishWaitSeconds,
                CASE WHEN lang.Id != 44 THEN 1 ELSE 0 END AS LotsCall,
                CASE WHEN lang.Id != 44 THEN child.WaitSeconds ELSE 0 END AS LotsWaitSeconds,
                CASE 
                    WHEN req.RequestStatusCodeId = 1 THEN "New"
                    WHEN req.RequestStatusCodeId = 2 THEN "In Service"
                    ELSE CASE
                        WHEN master.ServiceItemStatusCodeId = 3 THEN "Pending"
                        ELSE CASE
                            WHEN child.ServiceSeconds > 0 THEN "Serviced"
                            ELSE "Cancelled"
                        END
                    END
                END AS Status
            FROM 
                voyce.serviceitemmaster AS master 
            INNER JOIN 
                voyce.serviceitemdetail AS child ON child.ServiceItemMasterId = master.Id
            INNER JOIN 
                voyce.request AS req ON req.Id = child.RequestId
            INNER JOIN 
                voyce.language AS lang ON lang.Id = child.TargetLanguageId
            LEFT JOIN 
                voyce.requesteval AS eva ON eva.RequestId = req.Id AND EvalQuestionId = 1
            LEFT JOIN 
                voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId
            WHERE 
                master.RequestTime >= '{now2}' AND master.RequestTime <= '{now1}'
            ORDER BY
                master.RequestTime DESC
            """
        # try:
        #     with self.client0.cursor() as cursor:
        #         cursor.execute(query)
        #         result = cursor.fetchall()
        #         print(result)
        #         return result
        # except Exception as e:
        #     print("An error occurred while executing the query:", e)
        #     return None
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                total_price_sum = 0
                total_waiting_seconds_spanish_audio = 0
                spanish_audio_video_calls_count = 0
                total_waiting_seconds_other_languages_video = 0
                other_languages_video_calls_count = 0

                # Инициализация переменных статусов
                pending = 0
                new = 0
                in_service = 0
                serviced = 0
                cancelled = 0

                for row in result:
                    if 'TotalPrice' in row and row['TotalPrice'] is not None:
                        total_price_sum += row['TotalPrice']
                    total_price_sum = round(total_price_sum, 2)

                    if row['Language'] == 'Spanish' and row['CallType'] == 'Video' and row[
                        'Status'] == 'Serviced':
                        total_waiting_seconds_spanish_audio += row['WaitSeconds'] or 0
                        spanish_audio_video_calls_count += 1

                    if row['CallType'] == 'Video' and row['Status'] == 'Serviced' and row['Language'] not in [
                        'Spanish']:
                        total_waiting_seconds_other_languages_video += row['WaitSeconds'] or 0
                        other_languages_video_calls_count += 1

                    # Подсчет статусов
                    if row['Status'] == 'Pending':
                        pending += 1
                    elif row['Status'] == 'New':
                        new += 1
                    elif row['Status'] == 'In Service':
                        in_service += 1
                    elif row['Status'] == 'Serviced':
                        serviced += 1
                    elif row['Status'] == 'Cancelled':
                        cancelled += 1

                total_calls_serviced = cancelled + serviced
                minutes_used = sum(row['ServiceMinutes'] or 0 for row in result)
                completed_audio_calls = serviced - spanish_audio_video_calls_count - other_languages_video_calls_count

                if spanish_audio_video_calls_count > 0:
                    average_waiting_time_per_spanish_video_call = round(
                        total_waiting_seconds_spanish_audio / spanish_audio_video_calls_count)
                else:
                    average_waiting_time_per_spanish_video_call = 0

                if other_languages_video_calls_count > 0:
                    avg_waiting_seconds_video_ol = round(
                        total_waiting_seconds_other_languages_video / other_languages_video_calls_count)
                else:
                    avg_waiting_seconds_video_ol = 0

                if total_calls_serviced > 0:
                    avg_call_length_mins = round(minutes_used / total_calls_serviced)
                else:
                    avg_call_length_mins = 0

                # Вывод общей информации
                print(f"Total Price Sum: {total_price_sum}")
                print(f"Average Waiting Time per Spanish Video Call: {average_waiting_time_per_spanish_video_call}")
                print(f"AVG Wait Seconds Video (Other Languages): {avg_waiting_seconds_video_ol}")
                print(
                    f"Pending: {pending}, New: {new}, In Service: {in_service}, Serviced: {serviced}, Cancelled: {cancelled}")
                print(f"Total Calls Serviced (Cancelled + Serviced): {total_calls_serviced}")
                print(f"Completed Video Calls: {spanish_audio_video_calls_count + other_languages_video_calls_count}")
                print(f"Completed Audio Calls: {completed_audio_calls}")
                print(f"Minutes Used: {minutes_used}")
                print(f"Avg Call Length Mins: {avg_call_length_mins}")

                return total_price_sum, other_languages_video_calls_count, spanish_audio_video_calls_count, pending, new, in_service, serviced, cancelled, total_calls_serviced, completed_audio_calls, minutes_used, average_waiting_time_per_spanish_video_call, avg_waiting_seconds_video_ol, avg_call_length_mins
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    def query_all_data_widgets_by_periods(self, time_period):
        print("Starting to execute the query for time period:", time_period)

        now = datetime.now()
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)

        if time_period == 'yesterday':
            yesterday = now - timedelta(days=1)
            date_condition = f"master.RequestTime >= '{yesterday.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{now.strftime('%Y-%m-%d %H:%M:%S')}'"
            print(yesterday)
            print(now)
        elif time_period == 'this_week':
            start_of_week = now - timedelta(days=6)
            date_condition = f"master.RequestTime >= '{start_of_week.strftime('%Y-%m-%d %H:%M:%S')}'"
            print(start_of_week)
        elif time_period == 'last_week':
            start_of_last_week = now - timedelta(days=now.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"master.RequestTime >= '{start_of_last_week.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{(end_of_last_week + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            next_month = start_of_month + timedelta(days=31)
            start_of_next_month = next_month.replace(day=1)
            date_condition = f"master.RequestTime >= '{start_of_month.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{start_of_next_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_30_days':
            thirty_days_ago = now - timedelta(days=30)
            date_condition = f"master.RequestTime >= '{thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_month':
            first_day_current_month = now.replace(day=1)
            last_day_previous_month = first_day_current_month - timedelta(days=1)
            first_day_previous_month = last_day_previous_month.replace(day=1)
            date_condition = f"master.RequestTime >= '{first_day_previous_month.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{first_day_current_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1)
            date_condition = f"master.RequestTime >= '{start_of_year.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_year':
            start_of_last_year = (now.replace(month=1, day=1) - timedelta(days=1)).replace(month=1, day=1)
            end_of_last_year = start_of_last_year.replace(year=start_of_last_year.year + 1)
            date_condition = f"master.RequestTime >= '{start_of_last_year.strftime('%Y-%m-%d %H:%M:%S')}' AND master.RequestTime < '{end_of_last_year.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            print("Unknown time period.")
            return None

        query = f"""SELECT child.Id AS Id, child.RequestId AS ReferenceTransactionId, CEIL(child.ServiceSeconds/60) AS ServiceMinutes,
       master.RequestTime AS RequestTime, date_format(master.RequestTime, 'HH:mm:ss') AS ExtractedTime,
       timezone.TimeZoneId AS Timezone, master.ClientUserId AS UserId, master.ClientUserName AS UserName,
       child.ProviderFirstName AS InterpreterFirstName, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds,
       master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId,
       lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup,
       child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption,
       CASE WHEN master.CallerId IS NULL OR master.CallerId = '' THEN 'Application' ELSE master.CallerId END AS CallerID,
       child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName,
       q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice,
       CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service'
       ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0
       THEN 'Serviced' ELSE 'Cancelled' END END END AS Status
FROM voyce.serviceitemmaster AS master
INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId
INNER JOIN voyce.request AS req ON child.RequestId = req.Id
INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId
INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId
LEFT JOIN voyce.requesteval AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1
LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId
LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId
LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId
LEFT JOIN voyce.RequestPrice AS rp ON rp.RequestId = child.RequestId
WHERE {date_condition} AND NOT lang.EnglishName ILIKE '%Operator%' AND master.RequestCompanyId = 1673
ORDER BY master.RequestTime DESC"""

        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

                total_price_sum = 0
                total_waiting_seconds_spanish_audio = 0
                spanish_audio_video_calls_count = 0
                total_waiting_seconds_other_languages_video = 0
                other_languages_video_calls_count = 0

                # Инициализация переменных статусов
                pending = 0
                new = 0
                in_service = 0
                serviced = 0
                cancelled = 0

                for row in result:
                    if 'TotalPrice' in row and row['TotalPrice'] is not None:
                        total_price_sum += row['TotalPrice']
                    total_price_sum = round(total_price_sum, 2)

                    if row['TargetLanguage'] == 'Spanish' and row['VideoOption'] == 'Video' and row[
                        'Status'] == 'Serviced':
                        total_waiting_seconds_spanish_audio += row['WaitingSeconds'] or 0
                        spanish_audio_video_calls_count += 1

                    if row['VideoOption'] == 'Video' and row['Status'] == 'Serviced' and row['TargetLanguage'] not in [
                        'Spanish']:
                        total_waiting_seconds_other_languages_video += row['WaitingSeconds'] or 0
                        other_languages_video_calls_count += 1

                    # Подсчет статусов
                    if row['Status'] == 'Pending':
                        pending += 1
                    elif row['Status'] == 'New':
                        new += 1
                    elif row['Status'] == 'In Service':
                        in_service += 1
                    elif row['Status'] == 'Serviced':
                        serviced += 1
                    elif row['Status'] == 'Cancelled':
                        cancelled += 1

                total_calls_serviced = cancelled + serviced
                minutes_used = sum(row['ServiceMinutes'] or 0 for row in result)
                completed_audio_calls = serviced - spanish_audio_video_calls_count - other_languages_video_calls_count

                if spanish_audio_video_calls_count > 0:
                    average_waiting_time_per_spanish_video_call = round(
                        total_waiting_seconds_spanish_audio / spanish_audio_video_calls_count)
                else:
                    average_waiting_time_per_spanish_video_call = 0

                if other_languages_video_calls_count > 0:
                    avg_waiting_seconds_video_ol = round(
                        total_waiting_seconds_other_languages_video / other_languages_video_calls_count)
                else:
                    avg_waiting_seconds_video_ol = 0

                if total_calls_serviced > 0:
                    avg_call_length_mins = round(minutes_used / total_calls_serviced)
                else:
                    avg_call_length_mins = 0

                # Вывод общей информации
                print(f"Total Price Sum: {total_price_sum}")
                print(f"Average Waiting Time per Spanish Video Call: {average_waiting_time_per_spanish_video_call}")
                print(f"AVG Wait Seconds Video (Other Languages): {avg_waiting_seconds_video_ol}")
                print(
                    f"Pending: {pending}, New: {new}, In Service: {in_service}, Serviced: {serviced}, Cancelled: {cancelled}")
                print(f"Total Calls Serviced (Cancelled + Serviced): {total_calls_serviced}")
                print(f"Completed Video Calls: {spanish_audio_video_calls_count + other_languages_video_calls_count}")
                print(f"Completed Audio Calls: {completed_audio_calls}")
                print(f"Minutes Used: {minutes_used}")
                print(f"Avg Call Length Mins: {avg_call_length_mins}")

                return total_price_sum, other_languages_video_calls_count, spanish_audio_video_calls_count, pending, new, in_service, serviced, cancelled, total_calls_serviced, completed_audio_calls, minutes_used, average_waiting_time_per_spanish_video_call, avg_waiting_seconds_video_ol, avg_call_length_mins
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    def query_star_rating(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where master.RequestTime >= '{now1}' and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 and master.CallerId = '' and lang.EnglishName NOT ilike '%Operator%' and master.RequestCompanyId = 1673 order by master.RequestTime desc"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_cod(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"SELECT ANY_VALUE(master.RequestId) AS referencetransactionid, q2.PropertyValue AS IOSSerialNumber, ANY_VALUE(master.RequestTime) AS RequestTime, SUM(CEIL(child.ServiceSeconds / 60)) as ServiceMinutes, ANY_VALUE(master.ClientId) as ClientId, ANY_VALUE(master.RequestCompanyId) as CompanyId, COUNT(*) AS NumberOfServices FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request as req on child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE NOT ISNULL(q2.PropertyValue) AND NOT ISNULL(master.RequestId) AND NOT ISNULL(master.RequestTime) AND NOT ISNULL(master.ClientId) AND NOT ISNULL(master.RequestCompanyId) AND master.RequestTime >= '{now1}' AND req.RequestStatusCodeId not in (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1673 GROUP BY q2.PropertyValue HAVING IOSSerialNumber is not null"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_vod(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"SELECT ANY_VALUE(master.RequestId) AS referencetransactionid, q2.PropertyValue AS IOSSerialNumber, ANY_VALUE(master.RequestTime) AS RequestTime, SUM(CEIL(child.ServiceSeconds / 60)) AS ServiceMinutes, ANY_VALUE(master.ClientId) AS ClientId, ANY_VALUE(master.RequestCompanyId) AS CompanyId, COUNT(*) AS NumberOfServices FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id LEFT JOIN voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE NOT ISNULL(q2.PropertyValue) AND NOT ISNULL(master.RequestId) AND NOT ISNULL(master.RequestTime) AND NOT ISNULL(master.ClientId) AND NOT ISNULL(master.RequestCompanyId) AND master.RequestTime >= '{now1}' AND req.RequestStatusCodeId NOT IN (1, 2) AND master.ServiceItemStatusCodeId != 3 AND master.RequestCompanyId = 1673 GROUP BY q2.PropertyValue HAVING IOSSerialNumber IS NOT NULL"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_min_used(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"select child.Id as Id, child.RequestId as ReferenceTransactionId, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserId as UserId, master.ClientUserName as UserName, child.ProviderFirstName as InterpreterFirstName, master.RowDate as Date, child.WaitSeconds as WaitingSeconds, master.RequestCompanyId as CompanyId, master.ClientName as ClientName, child.ProviderId as InterpreterId, lang.EnglishName as TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime as ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') as VideoOption, case when (master.CallerId is null or master.CallerId = '') then 'Application' else master.CallerId end as CallerID, child.CancelTime as ServiceCancelTime, eval.Answer as CallQualityRatingStar, companyProduct.Name as RequestProductName, q2.PropertyValue AS IOSSerialNumber, rp.TotalPrice, case when req.RequestStatusCodeId = 1 then 'New' when req.RequestStatusCodeId = 2 then 'In Service' else case when master.ServiceItemStatusCodeId = 3 then 'Pending' else case when child.ServiceSeconds > 0 then 'Serviced' else 'Cancelled' end end end as Status from voyce.serviceitemmaster as master inner join voyce.serviceitemdetail as child on master.id = child.ServiceItemMasterId inner join voyce.request as req on child.RequestId = req.Id inner join voyce.billcompanyproduct as companyProduct on companyProduct.Id = master.RequestBillCompanyProductId inner join voyce.language as lang on lang.Id = child.TargetLanguageId left join voyce.requesteval as eval on eval.RequestId = child.RequestId and eval.EvalQuestionId = 1 left join voyce.companytimezone as timezone on master.RequestCompanyId = timezone.CompanyId left join voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId left join voyce.personsessionproperty_serialnumber AS q2 ON q2.PersonSessionId = q1.PersonSessionId left join voyce.RequestPrice as rp on rp.RequestId = child.RequestId where master.RequestTime >= '{now1}' and req.RequestStatusCodeId not in (1, 2) and master.ServiceItemStatusCodeId != 3 and lang.EnglishName NOT ilike '%Operator%' and master.ClientId in (49957,51037,51378,51379,51380,52864) and master.RequestCompanyId = 1604 order by master.RequestTime desc"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

    def query_top_languages_by_period(self, time_period):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=5, minute=0, second=0, microsecond=0)  # Обнуляем время для корректного сравнения дат

        # Определение date_condition в зависимости от time_period
        if time_period == 'yesterday':
            yesterday = now - timedelta(days=1)
            date_condition = f"a.Date >= '{yesterday.strftime('%Y-%m-%d %H:%M:%S')}' AND a.Date < '{now.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_week':
            start_of_week = (now - timedelta(days=now.weekday()))
            date_condition = f"a.Date >= '{start_of_week.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_week':
            start_of_last_week = (now - timedelta(days=now.weekday() + 7))
            end_of_last_week = start_of_last_week + timedelta(days=6)
            date_condition = f"a.Date >= '{start_of_last_week.strftime('%Y-%m-%d %H:%M:%S')}' AND a.Date < '{end_of_last_week.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_month':
            start_of_month = now.replace(day=1)
            date_condition = f"a.Date >= '{start_of_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_30_days':
            thirty_days_ago = now - timedelta(days=30)
            date_condition = f"a.Date >= '{thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'last_month':
            start_of_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
            end_of_last_month = now.replace(day=1)
            print(start_of_last_month)
            print(end_of_last_month)
            date_condition = f"a.Date > '{start_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}' AND a.Date < '{end_of_last_month.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif time_period == 'this_year':
            start_of_year = now.replace(month=1, day=1)
            print(start_of_year)
            date_condition = f"a.Date >= '{start_of_year.strftime('%Y-%m-%d %H:%M:%S')}'"

        elif time_period == 'last_year':
            start_of_last_year = now.replace(year=now.year - 1, month=1, day=1)
            end_of_last_year = now.replace(month=1, day=1) - timedelta(days=1)
            date_condition = f"a.Date >= '{start_of_last_year.strftime('%Y-%m-%d %H:%M:%S')}' AND a.Date < '{end_of_last_year.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            date_condition = "1=1"  # В случае неизвестного периода, запрос возвращает данные за все время

        query = f"""
        SELECT a.TargetLanguage, 
               SUM(a.ServiceMinutes) as ServiceMinutes, 
               SUM(a.WaitingSeconds) as WaitingSeconds, 
               SUM(a.TotalCalls) as TotalCalls, 
               SUM(a.CountSuccessAudioCalls) as CountSuccessAudioCalls, 
               SUM(a.CountSuccessVideoCalls) as CountSuccessVideoCalls, 
               SUM(a.CountFailedAudioCalls) as CountFailedAudioCalls, 
               SUM(a.CountFailedVideoCalls) as CountFailedVideoCalls, 
               SUM(a.CountAudioMinute) as CountAudioMinute, 
               SUM(a.CountVideoMinute) as CountVideoMinute, 
               SUM(a.CountPendingAudioCalls) as CountPendingAudioCalls, 
               SUM(a.CountPendingVideoCalls) as CountPendingVideoCalls, 
               SUM(a.CountInServiceAudioCalls) as CountInServiceAudioCalls, 
               SUM(a.CountInServiceVideoCalls) as CountInServiceVideoCalls, 
               SUM(a.CountNewAudioCalls) as CountNewAudioCalls, 
               SUM(a.CountNewVideoCalls) as CountNewVideoCalls, 
               SUM(a.CountBackupCalls) as CountBackupCalls, 
               SUM(a.BackupWaitingSeconds) as BackupWaitingSeconds, 
               SUM(a.CallQualityRatingStar) as CallQualityRatingStar, 
               SUM(a.CountRatingStarCalls) as CountRatingStarCalls 
        FROM voyce.aggbyclient as a 
        WHERE a.CompanyId = 1355 AND {date_condition} 
        GROUP BY a.TargetLanguage 
        ORDER BY ServiceMinutes DESC 
        LIMIT 5;
        """

        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print("Произошла ошибка при выполнении запроса:", e)
            return None

    def query_check1(self):
        now = datetime.now()  # Текущее время
        now = now.replace(hour=6, minute=0, second=0, microsecond=0)
        now1 = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"select main.Id as InterpreterId, any_value(main.Name) as FirstName, any_value(main.LastName) as LastName, CONCAT(any_value(main.Name), ' ', any_value(main.LastName)) as InterpreterName, any_value(main.CreateDate) as InterpreterJoinDate, any_value(c.CompanyCode) as CompanyCode, any_value(c.Id) as CompanyId, case when any_value(txn.RequestId) is not null then 'In conference' when any_value(pos.ProviderOnlineStatusCodeId) = 1 then 'Online' else 'Offline' end as Status, any_value(txn.RequestId) as RequestId, array_distinct( array_union( collect_set(lang1.EnglishName), collect_set(lang2.EnglishName) ) ) as Languages from voyce.provider as main left join voyce.providerservice as service on main.Id = service.ProviderId left join voyce.Language as lang1 on service.LanguageId1 = lang1.Id left join voyce.Language as lang2 on service.LanguageId2 = lang2.Id left join voyce.lspprovider as lsp on main.Id = lsp.ProviderId left join voyce.company as c on lsp.CompanyId = c.Id left join ( select child.RequestId, child.ProviderId from voyce.serviceitemdetail as child inner join voyce.request as req on child.RequestId = req.Id inner join voyce.serviceitemmaster as master on master.Id = child.ServiceItemMasterId where req.RequestStatusCodeId in (1, 2) ) as txn on txn.ProviderId = main.Id left join ( SELECT pos.*, ROW_NUMBER() OVER ( PARTITION BY pos.ProviderId ORDER BY pos.LastUpdate DESC ) AS rn FROM voyce.provideronlinestatus AS pos ) AS pos ON pos.ProviderId = main.Id AND pos.rn = 1 where main.Available = true and service.Deleted = false and service.Active = true and main.Name not ilike '%test%' and main.LastName not ilike '%test%' and c.Id in (1265, 1058, 1679, 1404, 1053, 1398, 1264, 1032, 1601, 1033, 1080, 1846) group by main.Id"
        try:
            with self.client0.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)

                # Запись данных в файл
                with open('query_results.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in cursor.description])  # Заголовки столбцов
                    writer.writerows(result)
                print(result)
                return result
        except Exception as e:
            print("An error occurred while executing the query:", e)
            return None

# db_instance = Databricks()
# language = "Yoruba"
# time_period = 'This_week'
# result = db_instance.query_transactions_periods_Admin_PROD('yesterday')
