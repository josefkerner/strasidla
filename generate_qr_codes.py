import qrcode
from PIL import Image
import PIL
from PyPDF2 import PdfReader, PdfWriter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from tqdm import tqdm

INDEX = 1

def get_qr_code_img(i:int):
    img = qrcode.make('StrasidlaHlidka:{}'.format(i))
    im = img.resize((125, 125))
    filename = f"images/qr_code_{i}.png"
    img.save(filename)
    #im = Image.open("qr_code.png")
    #resize image to 100x100 pixels

    return filename


def write_qr_codes(existing_pdf,i:int, index:int):
    packet = io.BytesIO()

    # do whatever writing you want to do
    can = canvas.Canvas(packet, pagesize=A4)
    img1 = get_qr_code_img(index)
    index = index + 1
    img2 = get_qr_code_img(index)
    index = index + 1
    img3 = get_qr_code_img(index)
    index = index + 1
    img4 = get_qr_code_img(index)


    #0,0 is bottom left corner

    can.drawImage(image=img1, x=0, y=600, width=100, height=100, anchor='sw')
    #write img2 to the top right corner
    can.drawImage(image=img2, x=300, y=600, width=100, height=100, anchor='sw')
    #write img3 to the bottom left corner
    can.drawImage(image=img3, x=0, y=180, width=100, height=100, anchor='sw')
    #write img4 to the bottom right corner
    can.drawImage(image=img4, x=300, y=180, width=100, height=100, anchor='sw')

    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[i]
    page.merge_page(new_pdf.pages[0])
    return page, index


def write_file():
    images = []
    for i in range(0,10):

        img = qrcode.make(f'Hlidka {i} strasidla')
        #save image to png file
        img.save(f'hlidka_{i}.png')
        #open image file
        im = PIL.Image.open(f"hlidka_{i}.png").convert("RGB")

        images.append(im)
    #create blank image
    im1 = PIL.Image.new("RGB", (300, 300))
    im1.save("out_all.pdf", save_all=True, append_images=images)


def write_text(existing_pdf, i: int, start: str):
    packet = io.BytesIO()

    # do whatever writing you want to do
    can = canvas.Canvas(packet, pagesize=A4)

    can.drawString(70, 10, f"Hlidka {i}, start: {start}")
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)


    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[i]
    page.merge_page(new_pdf.pages[0])
    return page




def process_pdf(BASE_INDEX):
    output = PdfWriter()
    ex_file = "startovni_karty.pdf"
    existing_pdf = PdfReader(open(ex_file, "rb"))
    #number of pages
    num_pages = len(existing_pdf.pages)
    #generatelist from 0 to num_pages
    page_indexes = list(range(num_pages))
    print(num_pages)
    INDEX = BASE_INDEX

    for i in tqdm(page_indexes):
        page, ind = write_qr_codes(existing_pdf, i,INDEX)
        INDEX = ind
        #page = write_text(existing_pdf, i, start="10:00")
        output.add_page(page)

    # finally, write "output" to a real file
    outputStream = open("hlidky.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

#write_file()
process_pdf(BASE_INDEX=INDEX)

