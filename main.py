# import package fastapi
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

# variabel untuk auth key
password = "secret123"

# create FastAPI object
app = FastAPI()

# endpoint -> alamat tertentu yg bisa diakses oleh client
# create endpoint to get data from main page
# endpoint dan function handler selalu beriringan
@app.get("/")
def get_home(): #function handler -> utk menghandle request dari endpoint tertentu
    return {
        "message" : "Hello World!"
    }

# endpoint untuk ngambil data dari csv
@app.get("/data")
def get_csv(): #nama fungsi bisa tetap sama karena ini udah otomatis nempel ke endpoint, tp dibedain jg gpp
    # 1. baca data dari csv
    df = pd.read_csv("data.csv")
    # 2. tampilkan response berupa data csv menjadi json
    return df.to_dict(orient="records")

# endpoint untuk ngambil data tapi by name
@app.get("/data/{name}")
def get_by_name(name):
    # 1. baca data dari csv
    df = pd.read_csv("data.csv")
    # 2. filter data by name
    result = df[df['name'] == name]
    # cek apakah hasil filter > 0 (ada)
    if len(result) > 0:
        # 3. display response berupa data by name berupa json
        return result.to_dict(orient="records")
    else:
        #tampilkan pesan error
        raise HTTPException(status_code=404, detail=f"Data {name} tidak ditemukan.")

# endpoint untuk delete data dari csv
@app.delete("/data/{name}")
def delete_by_name(name: str, api_key: str = Header(None)):
    # check auth
    if api_key != None and api_key == password:
        # 1. baca data dari csv
        df = pd.read_csv("data.csv")
        # 2. filter data by name
        result = df[~(df['name'] == name)]
        # replace csv excisting -> data yang difilter akan hilang
        result.to_csv("data.csv", index = False)
        # 3. display response berupa data by name berupa json
        return result.to_dict(orient="records")
    else:
        raise HTTPException(status_code=403, detail="Password salah.")
    
# put -> update data, data berubah tapi jumlah tetap sama
# post -> menambahkan data, jumlah data bertambah