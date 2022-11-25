import pretty_table_generator
import pdf_generator

key = input("Напишите 1, если хотите сгенерировать таблицу. Напишите 2, если хотите сформировать pdf ")
if (key == "1"):
    pretty_table_generator.get_pretty_table()
elif (key == "2"):
    pdf_generator.get_pdf_statistic()