
![](/assets/cover.png)

<p align="center">
    <p><a href="https://github.com/jackeyGao/dayone2PDF"<b>dayone2PDF</b></a> is a script for convert your dayone journal to pdf book. </p>

    <p>dayone2PDF is just render html using dayone export file then print the PDF with pyQt5.</p>
</p>


## Requirements

- PyQt5==5.11.3 
- Jinja2
- PyPDF2  

More please view [`requirements.txt`](/requirements.txt) file.

## Usage


```shell
git clone https://github.com/jackeyGao/dayone2PDF
pip install -r requirements.txt
```


**1. Export dayone**


Export dayone data from dayone app. unzip to current directory. then rename is `./dayone`.


So, The directory structure should be like this:

```
.
├── assets
├── create_pdf.py
├── dayone          # The dayone export directory.
    ├── 2018.json
    ├── ...         # Your journal set such as ***.json.
    └── photos/     # Your journal photos.
├── md.py
├── pdfs
├── render.py
├── requirements.txt
└── templates
```


**2. Render HTML**

```shell
python render.py
```


**3. Create PDF file of journal set**

```shell
python create_pdf.py output/2018.json

python create_pdf.py output/{ other set }.json
```

Will multiple pdf book if your journal set is multiple


## License


MIT License.




