import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Goodreads Reading Dashboard")

st.write("Upload your Goodreads CSV file to explore your reading habits.")

uploaded = st.file_uploader("Upload Goodreads CSV", type="csv")

if uploaded is not None:
    df = pd.read_csv(uploaded)

    st.subheader("Raw Data")
    st.dataframe(df)

    # Clean data
    df["Date Read"] = pd.to_datetime(df["Date Read"], errors="coerce")
    df["Year Read"] = df["Date Read"].dt.year

    st.subheader("Books Read Per Year")
    year_counts = df["Year Read"].value_counts().sort_index()
    fig = px.bar(year_counts, labels={"index": "Year", "value": "Books Read"})
    st.plotly_chart(fig)

    st.subheader("Ratings You Gave")
    fig2 = px.histogram(df, x="My Rating", nbins=5)
    st.plotly_chart(fig2)

    # Genre count if tags exist
    if "Bookshelves" in df.columns:
        st.subheader("Most Common Shelves / Genres")

        genre_series = (
            df["Bookshelves"]
            .str.split(",")
            .explode()
            .str.strip()
            .value_counts()
            .head(15)
        )

        fig3 = px.bar(
            genre_series,
            labels={"index": "Genre", "value": "Count"}
        )
        st.plotly_chart(fig3)

    st.subheader("Top Authors")
    author_counts = df["Author"].value_counts().head(15)
    fig4 = px.bar(author_counts, labels={"index": "Author", "value": "Books Read"})
    st.plotly_chart(fig4)

    st.subheader("Page Count Distribution")
    if "Number of Pages" in df.columns:
        fig5 = px.histogram(df, x="Number of Pages", nbins=20)
        st.plotly_chart(fig5)

    st.success("Dashboard loaded.")
