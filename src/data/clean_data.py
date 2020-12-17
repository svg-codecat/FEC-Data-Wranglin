import pandas as pd
import fnmatch

# Imports for ngrams()
import re
from ftfy import fix_text

# Imports for awesome_cossim_top()
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct

# Import for vectorize
from sklearn.feature_extraction.text import TfidfVectorizer

def _csv_to_df(path: str):
    df = pd.read_csv(f"data/raw_data/{path}", index_col=0)
    df.fillna(value="", inplace=True)
    return df
    
        

def _get_df_columns(df):
    column_list = df.columns.values.tolist()
    return column_list


class DataCleaner:
    

    def __init__(self, path: pd.DataFrame, lowest_similarity: float, column_name: str, ngram_size: int):
        self.df = path
        self.lowest_similarity = lowest_similarity
        self.column_name = column_name
        self.ngram_size = ngram_size
        

    def _ngrams(self, string):
        string = str(string)
        string = fix_text(string) # fix text
        string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
        string = string.lower()
        chars_to_remove = [")","(",".","|","[","]","{","}","'"]
        rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
        string = re.sub(rx, '', string)
        string = string.replace('&', 'and')
        string = string.replace(',', ' ')
        string = string.replace('-', ' ')
        string = string.title() # normalise case - capital at start of each word
        string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
        string = ' '+ string +' ' # pad names for ngrams...
        string = re.sub(r'[,-./]|\sBD',r'', string)
        ngrams = zip(*[string[i:] for i in range(self.ngram_size)])
        return [''.join(ngram) for ngram in ngrams]


    def _awesome_cossim_top(self, A, B, ntop):
        # force A and B as a CSR matrix.
        # If they have already been CSR, there is no overhead
        A = A.tocsr()
        B = B.tocsr()
        M, _ = A.shape
        _, N = B.shape  
 
        idx_dtype = np.int32
 
        nnz_max = M*ntop
 
        indptr = np.zeros(M+1, dtype=idx_dtype)
        indices = np.zeros(nnz_max, dtype=idx_dtype)
        data = np.zeros(nnz_max, dtype=A.dtype)

        ct.sparse_dot_topn(
            M, N, np.asarray(A.indptr, dtype=idx_dtype),
            np.asarray(A.indices, dtype=idx_dtype),
            A.data,
            np.asarray(B.indptr, dtype=idx_dtype),
            np.asarray(B.indices, dtype=idx_dtype),
            B.data,
            ntop,
            self.lowest_similarity,
            indptr, indices, data)

        return csr_matrix((data,indices,indptr),shape=(M,N))


    def _get_matches_df(self, sparse_matrix, name_vector):
        non_zeros = sparse_matrix.nonzero()
    
        sparserows = non_zeros[0]
        sparsecols = non_zeros[1]
    
        nr_matches = sparsecols.size
    
        left_side = np.empty([nr_matches], dtype=object)
        right_side = np.empty([nr_matches], dtype=object)
        similairity = np.zeros(nr_matches)

        for index in range(0, nr_matches):
            left_side[index] = name_vector[sparserows[index]]
            right_side[index] = name_vector[sparsecols[index]]
            similairity[index] = sparse_matrix.data[index]

        return pd.DataFrame({
                        'left_side': left_side,
                        'right_side': right_side,
                        'similairity': similairity
                        })


    def _replace_matches_df(self):
        unique_names = self.df[self.column_name].unique()
        #print(len(unique_names))
        vectorizer = TfidfVectorizer(min_df=1, analyzer=self._ngrams)
        tf_idf_matrix = vectorizer.fit_transform(unique_names)
        matches = self._awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), 10)
        matches_df = self._get_matches_df(matches, unique_names)
        matches_df = matches_df[matches_df['similairity'] < 0.99999] # Remove all exact matches
        for left_side, right_side in zip(matches_df['left_side'], matches_df['right_side']):
            for position, column in zip(self.df.index, self.df[self.column_name]):
                if column == right_side:
                    self.df.at[position, self.column_name] = left_side
        #print(len(self.df[self.column_name].unique()))
        return self.df


def build_classes(path: str, lowest_similarity: float, ngram_size: int):
    df = _csv_to_df(path)
    column_list = _get_df_columns(df)
    count = 0
    name_list = []
    for i in range(len(column_list)+1):
        name_list.append(f"cleaner{str(i)}")   
    replace = DataCleaner._replace_matches_df
    for column in column_list:
        print("Cleaning " + column + " column " + "of " + path)
        if count < 1:
            name_list[count] = DataCleaner(df, lowest_similarity, column, ngram_size)
            count += 1
            name_list[count-1]
        
        name_list[count] = DataCleaner(replace(name_list[count-1]), lowest_similarity, column, ngram_size)
        count += 1
        name_list[count-1]
    return replace(name_list[count-1])  

def return_df_as_csv(df, filename: str):
    df.to_csv(f"data/cleaned_data/{filename}")

