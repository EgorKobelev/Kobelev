import pretty_table_generator
import pdf_generator

user_choice = input("Напишите 1, если хотите сгенерировать таблицу. Напишите 2, если хотите сформировать pdf ")
if (user_choice == "1"):
    pretty_table_generator.get_pretty_table()
elif (user_choice == "2"):
    pdf_generator.get_pdf_statistic()