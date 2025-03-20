from enum import IntEnum, EnumMeta

class RedshiftOIDMeta(EnumMeta):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError(f"Cannot modify OID constant '{name}'")
            # throw error if any constant value defined in RedshiftOID was modified
            # e.g. "Cannot modify OID constant 'VARCHAR'"
        super().__setattr__(name, value)


class RedshiftOID(IntEnum, metaclass=RedshiftOIDMeta):
    ACLITEM = 1033
    ACLITEM_ARRAY = 1034
    ANY_ARRAY = 2277
    ABSTIME = 702
    BIGINT = 20
    BIGINT_ARRAY = 1016
    BOOLEAN = 16
    BOOLEAN_ARRAY = 1000
    BPCHAR = 1042
    BPCHAR_ARRAY = 1014
    BYTES = 17
    BYTES_ARRAY = 1001
    CHAR = 18
    CHAR_ARRAY = 1002
    CIDR = 650
    CIDR_ARRAY = 651
    CSTRING = 2275
    CSTRING_ARRAY = 1263
    DATE = 1082
    DATE_ARRAY = 1182
    FLOAT = 701
    FLOAT_ARRAY = 1022
    GEOGRAPHY = 3001
    GEOMETRY = 3000
    GEOMETRYHEX = 3999
    INET = 869
    INET_ARRAY = 1041
    INT2VECTOR = 22
    INTEGER = 23
    INTEGER_ARRAY = 1007
    INTERVAL = 1186
    INTERVAL_ARRAY = 1187
    INTERVALY2M = 1188
    INTERVALY2M_ARRAY = 1189
    INTERVALD2S = 1190
    INTERVALD2S_ARRAY = 1191
    JSON = 114
    JSON_ARRAY = 199
    JSONB = 3802
    JSONB_ARRAY = 3807
    MACADDR = 829
    MONEY = 790
    MONEY_ARRAY = 791
    NAME = 19
    NAME_ARRAY = 1003
    NUMERIC = 1700
    NUMERIC_ARRAY = 1231
    NULLTYPE = -1
    OID = 26
    OID_ARRAY = 1028
    POINT = 600
    REAL = 700
    REAL_ARRAY = 1021
    REGPROC = 24
    SMALLINT = 21
    SMALLINT_ARRAY = 1005
    SMALLINT_VECTOR = 22
    STRING = 1043
    SUPER = 4000
    TEXT = 25
    TEXT_ARRAY = 1009
    TIME = 1083
    TIME_ARRAY = 1183
    TIMESTAMP = 1114
    TIMESTAMP_ARRAY = 1115
    TIMESTAMPTZ = 1184
    TIMESTAMPTZ_ARRAY = 1185
    TIMETZ = 1266
    UNKNOWN = 705
    UUID_TYPE = 2950
    UUID_ARRAY = 2951
    VARCHAR = 1043
    VARBYTE = 6551
    VARCHAR_ARRAY = 1015
    XID = 28

    BIGINTEGER = BIGINT
    DATETIME = TIMESTAMP
    NUMBER = DECIMAL = NUMERIC
    DECIMAL_ARRAY = NUMERIC_ARRAY
    ROWID = OID


def get_datatype_name(oid: int) -> str:
    return RedshiftOID(oid).name
