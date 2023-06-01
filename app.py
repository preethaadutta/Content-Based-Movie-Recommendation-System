import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # it'll fetch the index position of that movie
    distances = similarity[movie_index]  # it'll calculate distance
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                  1:6]  # this line will extract first 5 movies
    # each time it'll take as tuple
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:  # this will print those 5 movie names and show that to user
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)  # we want to print the title of 1st similar five movies
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters




navbar='''
<head>
<script src="https://kit.fontawesome.com/dd58328c2f.js" crossorigin="anonymous"></script>
<link href="https://fonts.googleapis.com/css2?family=Satisfy&display=swap" rel="stylesheet">
<style>
    *{
        padding:0;
        margin:0;
        box-sizing:border-box;
    }
    html{
        display:flex;
    }
    @import url('https://fonts.googleapis.com/css2?family=Satisfy&display=swap');
    div.logo{
        color:#2691d9;
        font-size:35px;
        line-height:25px;
        padding-left:5px;
        font-family: 'Satisfy', cursive;
        font-weight:bold;
    }
    .logo span{
        color:rgb(238, 24, 60);
    }
    .menu{
        margin-right:20px;
    }
    /*
    .menu a:hover{
        background:transparent;
        background: rgba(255, 0, 0, 0.253);
        backdrop-filter: blur(2px);
        transition:0.3s;
        border-radius:10px;
    }
    */
    menu.a{
        margin:0;
        text-decoration:none;
        list-style:none;
        box-sizing:border-box;
    }
    #an
    {
        text-decoration:none;
        color:rgb(238, 24, 60);
        margin:0;
        padding:10px 10px;
        font-size:20px;
        font-family:'Roboto', Serif;
        font-weight:bold;
    }
    nav{
        /*background:linear-gradient(135deg,#FFFF00,#16E2F5);,#E30B5D*/
        background:transparent;
        background: rgba(255, 0, 0, 0.243);
        backdrop-filter: blur(2px);
        /*background:linear-gradient(135deg,#F778A1,#FFD801);*/
        height:60px;
        margin:0;
        width:100%;
        display:flex;
        justify-content:space-between;
        align-items:center;
    }
    a#an:hover{
        color:#2691d9;
    }
    @media screen and (max-width:768px){
        nav{
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        text-align: center;
        height:90px;
        }
        div.logo{
            padding-left:34%;
        }
        #an{
        flex-grow: 1;
        flex-basis: auto;
        flex-shrink: 0;
        }
        div.menu{
            padding-left:18%;
        }
    }
    @media screen and (max-width:590px){
        div.menu{
            padding-left:5%;
        }
    }
    @media screen and (max-width:531px){
        div.logo{
            font-size:120%;
        }
        #an{
            /*font-size:90%;*/
            font-size:14px;
            padding-right:5px;
            padding-left:5px;
        }
        div.menu{
            padding-left:5%;
        }
    }
    @media screen and (max-width:337px){
        #an{
            font-size:13px;
            padding-right:2px;
            padding-left:2px;
        }
        div.menu{
            padding-left:2%;
        }
    }
    @media screen and (max-width:264px){
        nav{
            height:300px;
        }
        div.logo{
            font-size:22px;
            display:block;
            padding-left:5%;
        }
        #an{
            display:block;
            font-size:20px;
        }
    }                                                          
</style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">Movie<span>Mania</span></div>
            <div class="menu">
                <a id="an" href="#">Home</a>
                <a id="an" href="#">Trending</a>
                <!--<a id="an" href="#">Watchlist</a>-->
                <a id="an" href="#">Sign In</a>
                <a id="an" href="http://127.0.0.1:5500/buy_plan.html">Buy Plan</a>
            </div>
        </nav>
    </header>
</body>
'''
st.markdown(navbar,unsafe_allow_html=True)


# streamlit page background image ( image must be in url format )
page_bg_img = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');

/*
.css-1n76uvr{
        gap:5rem;
    } 
*/
.css-12oz5g7 {
    flex: 1 1 0%;
    width: 100%;
    padding: 6rem 1rem 10rem;
    padding-top:0;/*navbar will go top*/
    /*
    padding-right:0;
    padding-left:0;
    */
    max-width: none;
}


#movie-recommender-system span{
    font-family: 'Roboto', serif;
    color: rgb(255, 255, 255);
}
.stSelectbox label {
    font-size: 18px;
    color: #fff;
    font-family: 'Roboto', serif;
}
.css-6awftf{
    top: 0;
    right: 0;
    transform: scale(0.8);
}
.css-o1jpvw:hover > .css-6awftf{
    opacity: 1;
    outline: none;
    top: 0;
    right: 0;
    transform: scale(0.8);
    color: rgb(255, 255, 255);
    transition: none 0s ease 0s;
}
.css-183lzff{
    font-family: 'Roboto', serif;
    color: #fff;
    font-size: 16px;
    font-weight:700;
}
.stButton button{
    position: relative !important;
    background: rgb(255, 255, 255);
    color: rgb(0 0 0);
    font-size: 18px;
    font-weight: bold;
    font-family: 'Roboto', serif;
    overflow: hidden;
}    
.stApp{
    background:linear-gradient(0deg, rgba(0, 0, 0, 0.311), rgba(5, 0, 0, 0.249)), url(https://cutewallpaper.org/21/kodi-backgrounds-1920x1080/Kodi-Hd-Wallpaper-26-images-on-Genchi.info.jpg);
    background-size: cover;
}

</>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

#st.title('Movie Mania')

selected_movie_name=st.selectbox(
'Type your favourite movie name',
movies['title'].values)

if st.button('Search'):
    names,posters=recommend(selected_movie_name)

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])



footer='''
    
    <style>
    /*.css-12oz5g7 {
        flex: 1 1 0%;
        width: 100%;
        padding: 6rem 1rem 10rem;
        max-width: 46rem;
        //max-width: 100vw; login,search button width increasing
    }*/
    /*.css-1v3fvcr{
        width:100vh;
    }*/
    
    footer{
        /*background:linear-gradient(135deg,#DF6589FF,#A74AC7,#FF69B4);*/
        width:100%;
        font-family:'Roboto', Serif;
        font-weight:bold;
        background:#feafbc;
        backdrop-filter: blur(2px);
    }
    #text{
        visibility:hidden;
    }
    footer.css-1q1n0ol.egzxvld4{
        text-align:center;
        color:#000000;
    }
    a.css-1vbd788.egzxvld3{
        visibility:hidden;
        font-size:0.1px; //--
    }
    footer:after{
        content:"PreethaaDutta 2022 - Your Entertainment Guide - All Rights Reserved";
        position:relative;
        text-align:center;
    }
    button.css-1cpxqw2.edgvbvh1{
        background:#2691d9;
        height:45px;
        /*width:82px;*/
        border:1px solid;
        border-radius:25px;
        font-size:18px;
        font-weight:700;
        cursor:pointer;
        outline:none;

        background: none;
        border: 2px solid rgb(238, 24, 60);
        color:#fff;
        text-transform: uppercase;
        font-weight: bold;
        font-size: 1rem;
    }
    button[kind="primary"]:hover{
        border-color:#fff;
        color:rgb(238, 24, 60);
        transition:.5s;
    }
    .css-1q1n0ol{
        max-width:none;/*footer part full screen*/
    }
    </style>

'''
st.markdown(footer,unsafe_allow_html=True)
