from IPython.display import display
from tqdm import tqdm


import pandas as pd
import requests

# Display the whole dataframe <15
pd.set_option("display.max_rows", 15)
pd.set_option("display.max_columns", None)


# Create helper function
def solr_request(core, params, silent=False):
    """Performs a single Solr request to the IMPC Solr API.

    Example query:
        num_found, df = solr_request(
        core='genotype-phenotype',
        params={
            'q': '*:*',  # Your query, '*' retrieves all documents
            'rows': 10,  # Number of rows to retrieve
            'fl': 'marker_symbol,allele_symbol,parameter_stable_id',  # Fields to retrieve
        }
    )
    
    Faceting query provides a summary of data distribution across the specified fields.
    Example faceting query:
        num_found, df = solr_request(
        core='genotype-phenotype',
        params={
            'q': '*:*',
            'rows': 0,
            'facet': 'on',
            'facet.field': 'zygosity',
            'facet.limit': 15,
            'facet.mincount': 1
        }
    )

    When querying the phenodigm core, pass 'q': 'type:...'
    Example phenodigm query: 
        num_found, df = solr_request(
        core='phenodigm',
        params={
            'q': 'type:disease_model_summary', # Pass the type within the core and filters.
            'rows': 5
        }
    )

    Args:
        core (str): name of IMPC solr core.
        params (dict): dictionary containing the API call parameters.
        silent (bool, optional): When True, displays: URL of API call, the number of found docs and a portion of the DataFrame. Defaults to False.


    Returns:
        num_found: Number of docs found.
        pandas.DataFrame: Pandas.DataFrame object with the information requested.
    """

    base_url = "https://www.ebi.ac.uk/mi/impc/solr/"
    solr_url = base_url + core + "/select"

    response = requests.get(solr_url, params=params)
    if not silent:
        print(f"\nYour request:\n{response.request.url}\n")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        num_found = data["response"]["numFound"]
        if not silent:
            print(f"Number of found documents: {num_found}\n")

        # For faceting query
        if params.get('facet') == 'on':
            # Extract and add faceting query results to the list
            facet_counts = data["facet_counts"]["facet_fields"][params["facet.field"]]
            # Initialize an empty dictionary
            faceting_dict = {}
            # Iterate over the list, taking pairs of elements
            for i in range(0, len(facet_counts), 2):
                # Assign label as key and count as value
                label = facet_counts[i]
                count = facet_counts[i + 1]
                faceting_dict[label] = [count]

            # Convert the list of dictionaries into a DataFrame and print the DataFrame
            df = pd.DataFrame.from_dict(
                    faceting_dict, orient="index", columns=["counts"]
                ).reset_index()
            # Rename the columns
            df.columns = [params["facet.field"], "count_per_category"]

        # For regular query
        else:
            # Extract and add search results to the list
            search_results = []
            for doc in data["response"]["docs"]:
                search_results.append(doc)
    
            # Convert the list of dictionaries into a DataFrame and print the DataFrame
            df = pd.DataFrame(search_results)
        
        if not silent:
            display(df)
        return num_found, df

    else:
        print("Error:", response.status_code, response.text)


# Batch request based on solr_request
def batch_request(core, params, batch_size):
    """Calls `solr_request` multiple times with `params` to retrieve results in chunk `batch_size` rows at a time.

    Passing parameter `rows` is ignored and replaced with `batch_size`

    Example query:
        df = batch_request(
            core="genotype-phenotype",
            params={
                'q': 'top_level_mp_term_name:"cardiovascular system phenotype" AND effect_size:[* TO *] AND life_stage_name:"Late adult"',
                'fl': 'allele_accession_id,life_stage_name,marker_symbol,mp_term_name,p_value,parameter_name,parameter_stable_id,phenotyping_center,statistical_method,top_level_mp_term_name,effect_size'
            },
            batch_size=100)

    Args:
        core (str): name of IMPC solr core.
        params (dict): dictionary containing the API call parameters.
        batch_size (int): Size of batches (number of docs) per request.

    Returns:
        pandas.DataFrame: Pandas.DataFrame object with the information requested.
    """

    if "rows" in "params":
        print(
            "WARN: You have specified the `params` -> `rows` value. It will be ignored, because the data is retrieved `batch_size` rows at a time."
        )
    # Determine the total number of rows. Note that we do not request any data (rows = 0).
    num_results, _ = solr_request(
        core=core, params={**params, "start": 0, "rows": 0}, silent=True
    )
    # Initialise everything for data retrieval.
    start = 0
    chunks = []
    # Request chunks until we have complete data.
    with tqdm(total=num_results) as pbar:  # Initialize tqdm progress bar.
        while start < num_results:
            # Update progress bar with the number of rows requested.
            pbar.update(batch_size)
            # Request chunk. We don't need num_results anymore because it does not change.
            _, df_chunk = solr_request(
                core=core,
                params={**params, "start": start, "rows": batch_size},
                silent=True,
            )
            # Record chunk.
            chunks.append(df_chunk)
            # Increment start.
            start += batch_size
    # Prepare final dataframe.
    return pd.concat(chunks, ignore_index=True)
