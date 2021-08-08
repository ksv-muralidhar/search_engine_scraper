import pandas as pd
from bs4 import BeautifulSoup
import requests as r
import streamlit as st

st.markdown('<h1>Search Engine Scraper</h1>', unsafe_allow_html=True)
query = st.text_input('', help='Enter the search string and hit Enter/Return')
query = query.replace(" ", "+")
if query:
    try:
        req = r.get(f"https://www.bing.com/search?q={query}",
                    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"})
        result_str = '<html>'
        if req.status_code == 200:
            bs = BeautifulSoup(req.content)
            search_result = bs.find_all("li", class_="b_algo")
            search_result = [str(i).replace("<strong>","") for i in search_result]
            search_result = [str(i).replace("</strong>","") for i in search_result]
            result_df = pd.DataFrame()
            for n,i in enumerate(search_result):
                individual_search_result = BeautifulSoup(i)
                h2 = individual_search_result.find('h2')
                href = h2.find('a').get('href')
                url_txt = h2.find('a').text
                description = individual_search_result.find('p').text
                result_df = result_df.append(pd.DataFrame({"Title": url_txt, "URL": href, "Description": description}, index=[n]))
                count_str = f'<b style="font-size:20px;">Bing Search returned {len(result_df)} results</b>'
                result_str += f'<table style="border: none;">'+\
                f'<tr style="border: none;"><h3><a href={href} target="_blank">{url_txt}</a></h3></tr>'+\
                f'<tr style="border: none;"><b style="color:green;">{href}</b></tr>'+\
                f'<tr style="border: none;">{description}</tr>'+\
                f'<tr style="border: none;"><td style="border: none;"></td></tr></tr>'
            result_str += '</table></html>'
                
        else:
            result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
            result_str = '<html></html>'
            count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
    except:
        result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
        result_str = '<html></html>'
        count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
    
    st.markdown(f'{count_str}', unsafe_allow_html=True)
    st.markdown(f'{result_str}', unsafe_allow_html=True)
    st.markdown('<h3>Data Frame of the above search result</h3>', unsafe_allow_html=True)
    st.dataframe(result_df)