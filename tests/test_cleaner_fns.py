from src.data.clean_data import DataCleaner, _get_df_columns
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, bsr_matrix, csc_matrix
import pytest
import os

# Getting test csv and turning into DataFrame, filling None values with empty string
test_df = pd.read_csv("tests/test.csv", index_col = 0)
test_df.fillna(value="", inplace=True)

# Getting column list from test_df
column_list = _get_df_columns(test_df)
testing = []
for column in column_list:
    test = DataCleaner(test_df, 0.9, column, 3)
    testing.append(test)

class TestColumns:
    def test_column_list(self):
        expected = ["contributor_occupation", "contributor_employer", "contributor_city", "contributor_state", "contributor_zip", "party"]

        result = _get_df_columns(test_df)
        assert expected == result

class TestNgrams:
    def test_ngram_size(self):
        expected = [' Te', 'Tes', 'est', 'sti', 'tin', 'ing', 'ng ']

        result = testing[0]._ngrams("testing")
        assert expected == result

    def test_ngram_casing(self):
        expected = [' Te', 'Tes', 'est', 'sti', 'tin', 'ing', 'ng ']

        result = testing[1]._ngrams("tEsTiNg")
        assert expected == result

    def test_ngram_char_removal(self):
        expected = [' Te', 'Tes', 'est', 'sti', 'tin', 'ing', 'ng ']

        result = testing[2]._ngrams("[t){e]s)t.i|n'g")
        assert expected == result

    def test_ngram_and_spacing(self):
        expected = [' An', 'And', 'nd ', 'd T', ' Te', 'Tes', 'est', 'sti', 'tin', 'ing', 'ng ']

        result = testing[3]._ngrams("&        testing")
        assert expected == result

    def test_ngram_remove_non_ascii(self):
        expected = [' Te', 'Tes', 'est', 'sti', 'tin', 'ing', 'ng ']

        result = testing[4]._ngrams("©testing≠")
        assert expected == result

class TestAwesomeCossimTop:
    def test_matrix_shapes(self):
        A = csr_matrix((3,3))
        B = csr_matrix((2,3))
        
        with pytest.raises(ValueError) as exc_info:
            testing[0]._awesome_cossim_top(A, B, ntop=10)
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "A matrix multiplication will be operated. A.shape[1] must be equal to B.shape[0]!"

    def test_matrix_zeros(self):
        A = csr_matrix((3,3))
        B = csr_matrix((3,3))

        expected = 0

        result = testing[1]._awesome_cossim_top(A, B, ntop=10).count_nonzero()
        assert expected == result

    def test_input_matrix_type(self, capsys):
        A = bsr_matrix((3,3))
        B = csc_matrix((3,3))
        expected = csr_matrix((3,3)).get_shape()

        result = testing[2]._awesome_cossim_top(A, B, ntop=10).get_shape()
        captured = capsys.readouterr().out
        assert expected == result
        assert captured == ""
        
class TestGetMatchesDf:
    def test_dataframe_return(self):
        sparse_matrix = csr_matrix((3,3))
        name_vector = [0,0,0]
        
        result = testing[0]._get_matches_df(sparse_matrix, name_vector)
        assert len(result["left_side"]) == len(result["right_side"])