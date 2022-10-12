from google.cloud import storage
from google.cloud import bigquery

storageClient = storage.Client()
bigqueryClient = bigquery.Client()


def save_html(path, imagen64):
    with open(f"tmp/{path}.html", "w") as F:
        F.write(f"""<!DOCTYPE html>
                <html>
                <head>
                    <title>Index</title>
                </head>
                <body>
                    <img src="data:image/png;base64,{imagen64}">
                </body>
                </html>""")

    bucket = storageClient.bucket("ulima-html-files")
    blob = bucket.blob(f"{path}.html")
    blob.upload_from_filename(f"tmp/{path}.html")
    print(f"{path}.html saved in Storage")


def get_html(name):
    # with open(f"tmp/{data}.html", "w") as F:
    #     F.write(data)

    bucket = storageClient.bucket("ulima-html-files")
    blob = bucket.blob(f"{name}.html")
    html = blob.download_as_text()
    return html


def save_bigquery(idTable, data):
    errors = bigqueryClient.insert_rows_json(
            idTable,data)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))