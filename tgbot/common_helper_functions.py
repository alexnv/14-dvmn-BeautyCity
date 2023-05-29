text_start = "Здравствуйте. \n\n " \
            "Этот бот поможет вам записаться на прием в наш салон красоты BeautyCity.\n\n" \
             "       <b>Это удобно, так как вы сами выбираете и видите результат:</b> \n" \
             " <b>Если вы хотите живого общения можно ппозвонить 8 800 555 35 35</b> \n" \
             "       <b>Меню:</b>  \n" \
             "<b>Помощь</b> - часто задаваемые вопросы \n" \
             "<b>Записаться</b> - Зарезервировать и оплатить процедуру\n " \
             "<b>Отзывы</b> - Честные мнения наших поситителей \n" \
             "<b>Контакты</b> - Контакты Директора и адрес салона красоты \n" \
             "<b>Выйти из бота</b> - выход из бота"

text_help = "Часто задаваемые вопросы: \n\n" \
            " <b>Какие процедуры можно сделать: </b> \n" \
            " - мейкап\n" \
            " - покраска волос\n" \
            " - маникюр\n" \
            " <b>Есть ли у нас сертификат на услуги?</b>\n" \
            "- Да, с ним можно ознакомиться на стенде\n" \
            " <b>Как к вам позвонить?</b>\n" \
            " В рабочее время 8 800 555 35 35\n"


text_Contacts = "Руководитель: Ольга Ольговна Ольгина\n " \
                "e-mail: xxxxxxxx.xxx \n " \
                "ICQ: xxxxxxxxx \n " \
                "Tel: 8 800 555 35 35 \n " \
                "Адрес салона: Дремучий лес, избушка на курьих ножках"


file_db = '../db.sqlite3'

sql_create_ssf_table = """ CREATE TABLE IF NOT EXISTS projects (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            chat_id text,
                                            client_name text,                    
                                            client_address text,                 
                                            client_phone text,                   
                                            storage text,                        
                                            start_date date,                     
                                            end_date date,                       
                                            space float,                         
                                            weight float,                        
                                            items text,                          
                                            price float,
                                            delivery_by_courier INTEGER); """

                                            # id INTEGER PRIMARY KEY AUTOINCREMENT,   он же номер бокса (также его можно использовать для формирования QR кода)
                                            # client_name text,                       ФИО клиента
                                            # client_address text,                    адрес
                                            # client_phone text,                      телефон
                                            # storage text,                           название склада
                                            # start_date date,                        дата начала хранения
                                            # end_date date,                          срок хранения (оплатил до этой даты)
                                            # space float,                            объем хранимых вещей
                                            # weight float,                           вес хранимых вещей
                                            # items text,                             список вещей
                                            # price float,                            стоимость хранения (до конца срока хранения)
                                            # delivery_by_courier INTEGER,            доставка курьером (да0/нет1/доставленр2)





