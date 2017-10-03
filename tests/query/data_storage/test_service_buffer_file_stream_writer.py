# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from unittest import mock
from decimal import Decimal
import uuid
import struct
import io
from psycopg2.extras import NumericRange, DateTimeRange, DateTimeTZRange, DateRange

from pgsqltoolsservice.query.data_storage.service_buffer_file_stream_writer import ServiceBufferFileStreamWriter
from pgsqltoolsservice.query.contracts import DbColumn
from pgsqltoolsservice.parsers import datatypes
import tests.utils as utils


class TestServiceBufferFileStreamWriter(unittest.TestCase):

    def setUp(self):

        self._file_stream = io.BytesIO()
        self._writer = ServiceBufferFileStreamWriter(self._file_stream)
        self._cursor = utils.MockCursor([tuple([11, 22, 33]), tuple([55, 66, 77])])

    def tearDown(self):
        pass

    def test_write_to_file(self):
        val = 5
        byte_array = bytearray(struct.pack("i", val))
        res = self._writer._write_to_file(self._file_stream, byte_array)
        self.assertEqual(res, 4)

    def test_write_null(self):
        res = self._writer._write_null()
        self.assertEqual(res, 0)

    def test_write_bool(self):
        test_value = True
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_BOOL
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(1, res)

    def test_write_float(self):
        test_value = 123.456
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_REAL
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(4, res)

    def test_write_int(self):
        test_value = 123456
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_INTEGER
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(4, res)

    def test_write_decimal(self):
        test_val = Decimal(123)
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_NUMERIC
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_val)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(4, res)

    def test_write_char(self):
        test_value = 'a'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_CHAR
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(1, res)

    def test_write_str(self):
        test_value = 'TestString'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_TEXT
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)

    def test_write_date(self):
        test_value = '2004/10/19'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_DATE
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)

    def test_write_time(self):
        test_value = '10:23:54'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_TIME
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)

    def test_write_time_with_timezone(self):
        test_value = '10:23:54+02'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_TIME_WITH_TIMEZONE
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)

    def test_write_datetime(self):
        test_value = '2004/10/19 10:23:54'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_TIMESTAMP
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)

    def test_write_timedelta(self):
        test_value = '3 days 04:05:06'
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_INTERVAL
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)

    def test_write_uuid(self):
        test_value = uuid.uuid4()
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_UUID
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(36, res)  # UUID standard len is 36

    def test_write_bytea(self):
        test_value = memoryview(b'TestString')
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_BYTEA
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value.tobytes()), res)

    def test_write_json(self):
        test_value = {"Name": "TestName", "Schema": "TestSchema"}
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_JSON
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(str(test_value)), res)

    def test_write_array(self):
        test_value = ["TestVal1", "TestVal2"]
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_ARRAY
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(str(test_value)), res)

    def test_write_int4range(self):
        test_value = NumericRange(10, 20)
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_INT4RANGE
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(str(test_value)), res)

    def test_write_tsrange(self):
        test_value = DateTimeRange("2014-06-08 12:12:45", "2016-07-06 14:12:08")
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_TSRANGE
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(str(test_value)), res)

    def test_write_tstzrange(self):
        test_value = DateTimeTZRange("2014-06-08 12:12:45+02", "2016-07-06 14:12:08+02")
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_TSTZRANGE
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(str(test_value)), res)

    def test_write_daterange(self):
        test_value = DateRange("2015-06-06", "2016-08-08")
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = datatypes.DATATYPE_DATERANGE
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(str(test_value)), res)

    def test_write_udt(self):
        test_value = "TestUserDefinedTypes"
        test_columns_info = []
        col = DbColumn()
        col.data_type_name = 'UserDefinedTypes'
        test_columns_info.append(col)
        mock_storage_data_reader = MockStorageDataReader(self._cursor, test_columns_info)
        mock_storage_data_reader.get_value = mock.MagicMock(return_value=test_value)

        res = self._writer.write_row(mock_storage_data_reader)
        self.assertEqual(len(test_value), res)


class MockType:
    def __enter__(cls):
        return cls

    def __exit__(cls, typ, value, tb):
        pass


class MockStorageDataReader(MockType):

    def __init__(self, cursor, columns_info):
        self._cursor = cursor
        self.columns_info = columns_info

    def get_value(self, i):
        pass
