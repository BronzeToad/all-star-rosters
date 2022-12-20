import google.cloud.bigquery as gcpBigQuery
import os.path as osPath

from google.cloud.bigquery.client import Client as bqClient
from icecream import ic

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper
from helpers.case_wizard import CaseWizard


BREAK = '\n\n------------------------------------------------'

# ============================================================================ #

class BigQueryLoader:

    ROOT_DIR = EnvHelper.get_root_dir()
    SCHEMA_DIR = osPath.join(ROOT_DIR, 'configs', 'bigquery_schemas')
    GCP_PROJECT = EnvHelper.get_gcp_project()
    GCP_BUCKET = EnvHelper.get_gcp_bucket()
    DEFAULT_JOB_CONFIG = DataHelper.get_json(folder=osPath.join(ROOT_DIR, 'configs'),
                                                filename='bigquery_defaults')
    
    def __init__(self,
                 data_source: str,
                 table_id: str,
                 **kwargs):
        
        self.data_source = data_source
        self.table_id = table_id
        self.DEFAULT_JOB_CONFIG.update(kwargs)
        self.allow_jagged_rows = self.DEFAULT_JOB_CONFIG['allow_jagged_rows']
        self.allow_quoted_newlines = self.DEFAULT_JOB_CONFIG['allow_quoted_newlines']
        self.autodetect = self.DEFAULT_JOB_CONFIG['autodetect']
        self.create_disposition = self.DEFAULT_JOB_CONFIG['create_disposition']
        self.field_delimiter = self.DEFAULT_JOB_CONFIG['field_delimiter']
        self.ignore_unknown_values = self.DEFAULT_JOB_CONFIG['ignore_unknown_values']
        self.labels = self.DEFAULT_JOB_CONFIG['labels']
        self.max_bad_records = self.DEFAULT_JOB_CONFIG['max_bad_records']
        self.null_marker = self.DEFAULT_JOB_CONFIG['null_marker']
        self.quote_character = self.DEFAULT_JOB_CONFIG['quote_character']
        self.schema_file = self.DEFAULT_JOB_CONFIG['schema_file']
        self.skip_leading_rows = self.DEFAULT_JOB_CONFIG['skip_leading_rows']
        self.source_format = self.DEFAULT_JOB_CONFIG['source_format']
        self.write_disposition = self.DEFAULT_JOB_CONFIG['write_disposition']
        self.filename = None
        self.gcp_dir = None
        self.gcp_filepath = None
        self.job_id_prefix = None
        self.destination = None
        self.schema = None
        self.job_config = None
        self.job_result = None
        self.job_details = None
        self.job_id = None
        
# ============================================================================ #
    
    @staticmethod
    def count_rows(destination: str) -> int:
        """Counts number of records in BigQuery table.
        Parameters
        ----------
        destination : str
            BigQuery table destination. -> _project_._dataset_._table_
        Returns
        -------
        count : int
            Count of records.
        """
        table = bqClient().get_table(destination)
        count = 0 if table.num_rows is None else table.num_rows
        return count
    
    @staticmethod
    def job_exists(job_id: str) -> bool:
        """Checks if BigQuery job exists in GCP.
        Parameters
        ----------
        job_id : str
            BigQuery job id.
        Returns
        -------
        job.exists : bool
            True if job exists, else False.
        """
        job = bqClient().get_job(job_id)
        return job.exists
            
    @staticmethod
    def check_job_status(job_id: str, destination: str, qry_type: str, out_lvl: str) -> None:
        """Checks status of Bigquery job.
        Parameters
        ----------
        job_id : str
            BigQuery job id.
        destination : str
            BigQuery table destination. -> _project_._dataset_._table_
        qry_type : str
            Type of Reporting Engine query.
        out_lvl : str
            Subtype of Reporting Engine query.
        Raises
        ------
        RuntimeError
            If BigQuery job does not exist.
        """
        if BigQueryLoader.job_exists(job_id):
            rows = BigQueryLoader.count_rows(destination)
            print(f'\nData for {qry_type}-{out_lvl} loaded successfully to BigQuery.')
            print(f'{destination} contains {rows} records after data load.')
        else:
            raise RuntimeError(f'Job {job_id} does not exist...')


# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source
    
    @data_source.setter
    def data_source(self, val) -> None:
        if val not in self.valid_data_sources:
            raise ValueError(f'Invalid data source: {val}')
        self._data_source = val
        
    
    @property
    def table_id(self) -> str:
        return self._table_id
    
    @table_id.setter
    def table_id(self, val: str) -> None:
        self._table_id = val

# ============================================================================ #
    
    @property
    def quote_character(self) -> str:
        return self._quote_character
    
    @quote_character.setter
    def quote_character(self, val: str) -> None:
        if val is None:
            val = "" if self.DEFAULT_JOB_CONFIG['field_delimiter'] == '|' else None
        self._quote_character = val
        
        
    @property
    def schema_filepath(self) -> str:
        return self._schema_filepath
    
    @schema_filepath.setter
    def schema_filepath(self, val: str) -> None:
        val = osPath.join(self.SCHEMA_DIR, self.data_source)
        self._schema_filepath = val
        
        
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, val) -> None:
        val = DataHelper.force_extension(self.table_id, 'csv')
        self._filename = val
        

    @property
    def gcp_dir(self) -> str:
        return self._gcp_dir
    
    @gcp_dir.setter
    def gcp_dir(self, val) -> None:
        val = osPath.join(self.GCP_BUCKET, self.data_source)
        self._gcp_dir = val
    
    
    @property
    def gcp_filepath(self) -> str:
        return self._gcp_filepath
    
    @gcp_filepath.setter
    def gcp_filepath(self, val) -> None:
        val = osPath.join(self.gcp_dir, self.filename)
        self._gcp_filepath = val
        
    
    @property
    def job_id_prefix(self) -> str:
        return self._job_id_prefix
    
    @job_id_prefix.setter
    def job_id_prefix(self, val) -> None:
        _source = CaseWizard.convert(self.data_source, from_case='snake_case', to_case='PascalCase')
        _table = CaseWizard.convert(self.table_id, from_case='snake_case', to_case='PascalCase')
        _timestamp = DataHelper.get_epoch_timestamp()        
        val = f'{_source}_{_table}_{_timestamp()}_'
        self._job_id_prefix = val
    
    
    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, val) -> None:
        val = f'{self.GCP_PROJECT}.{self.data_source}.{self.table_id}'
        self._destination = val
    
    
    @property
    def schema(self) -> dict:
        return self._schema
        
    @schema.setter
    def schema(self, val) -> None:
        val = DataHelper.get_json(folder=self.schema_filepath,
                                  filename=self.filename)
        self._schema = val
    
    
    @property
    def job_config(self):
        return self._job_config
        
    @job_config.setter
    def job_config(self, val) -> None:
        val = gcpBigQuery.job.LoadJobConfig(allow_jagged_rows=self.DEFAULT_JOB_CONFIG['allow_jagged_rows'],
                                            allow_quoted_newlines=self.DEFAULT_JOB_CONFIG['allow_quoted_newlines'],
                                            autodetect=self.DEFAULT_JOB_CONFIG['autodetect'],
                                            create_disposition=self.DEFAULT_JOB_CONFIG['create_disposition'],
                                            field_delimiter=self.DEFAULT_JOB_CONFIG['field_delimiter'],
                                            ignore_unknown_values=self.DEFAULT_JOB_CONFIG['ignore_unknown_values'],
                                            max_bad_records=self.DEFAULT_JOB_CONFIG['max_bad_records'],
                                            quote_character=self.DEFAULT_JOB_CONFIG['quote_character'],
                                            skip_leading_rows=self.DEFAULT_JOB_CONFIG['skip_leading_rows'],
                                            write_disposition=self.DEFAULT_JOB_CONFIG['write_disposition'])
        val.quote_character = self.quote_character
        val.schema = self.schema
        self._job_config = val
    
    
    @property
    def job_result(self):
        return self._job_result
        
    @job_result.setter
    def job_result(self, val) -> None:
        _job = gcpBigQuery.Client().load_table_from_uri(source_uris=self.gcp_filepath,
                                                        destination=self.destination,
                                                        job_id_prefix=self.job_id_prefix,
                                                        job_config=self.job_config,
                                                        timeout=300.0)
        val = _job.result()
        self._job_result = val
    
    
    @property
    def job_details(self):
        return self._job_details
        
    @job_details.setter
    def job_details(self, val) -> None:
        val = self.job_result.to_api_repr()
        self._job_details = val
    
    
    @property
    def job_id(self):
        return self._job_id
        
    @job_id.setter
    def job_id(self, val) -> None:
        val = self.job_result.job_id
        self._job_id = val

# ============================================================================ #

    # @classmethod



# ============================================================================ #

if __name__ == '__main__':
    print(f'{BREAK} Executing as standalone script...')
    