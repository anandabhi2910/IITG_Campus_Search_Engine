"""
parse_mess_menus.py
Parses all 13 hostel mess menus for August 2026.
Data extracted directly from PDF context (image-based PDFs).
Outputs: one doc per hostel per day + one summary per hostel
"""

import os

OUT_DIR = "/home/claude/search_engine/data/real"
MONTH = "August 2026"
DATE = "2026-08-01"

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

TIMINGS = "Breakfast 7:15 AM to 9:30 AM. Lunch 12:00 PM to 2:00 PM. Dinner 7:30 PM to 9:30 PM. Holiday timings: Breakfast 8AM-10:15AM, Lunch 12:15-2:30PM, Dinner 8PM-10PM."

def write_doc(filepath, source, date, title, body):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(f"SOURCE: {source}\n")
        f.write(f"DATE: {date}\n")
        f.write(f"TITLE: {title}\n")
        f.write(f"BODY: {body}\n")

# All 13 hostels with full weekly menus
# Format: hostel -> day -> {breakfast, lunch, dinner}
MENUS = {
    "Barak": {
        "Monday": {
            "breakfast": "Poori with Black Chana, Veg Poha with Sev and Chopped Veggies, Banana, Egg Bhurji / Paneer Bhurji / Boiled Egg",
            "lunch": "Bhindi Do Pyaza, Rajma Masala, Arhar Dal, Jeera Rice, Plain Roti + Butter Roti, Lassi, Boondi Raita / Curd, Chutney",
            "dinner": "Veg Kolhapuri, Aloo Soyabeen, Dal Makhani, Chutney, Lemon Water, Plain Roti + Butter Roti, Pickle"
        },
        "Tuesday": {
            "breakfast": "Aloo Onion Parantha with Curd & Pickle, Dahi Chiwda, Water Melon, Egg Bhurji / Paneer Bhurji / Boiled Egg",
            "lunch": "Aloo Choka (Fry), Veg Kadhai, Dal Tadka, Plain Roti + Butter Roti, Boondi Raita / Curd, Butter Milk",
            "dinner": "Chole Bhature, Amritsari Chole Masala, Aloo Carrot Beans Stir Fry, Dal Maharani, Lemon Water, Plain Roti + Butter Roti"
        },
        "Wednesday": {
            "breakfast": "Dosa Schezwan / Dosa Plain with Coconut Chutney + Sambar, Chowmein, Pear, Egg Bhurji / Sweet Corn / Boiled Egg",
            "lunch": "Jeera Aloo, Kadhi Pakoda, Chana Dal, Plain Roti + Butter Roti, Curd / Dahi Wada, Sweet Lassi",
            "dinner": "Kadai Paneer / Chicken Nizam Handi, Mix Dal, Dum Biryani, Ice Cream, Raita, Latcha Paratha, Plain Roti + Butter Roti"
        },
        "Thursday": {
            "breakfast": "Besan Cheela / Veg Roll, Veg Upma, Pine Apple, Egg Bhurji / Paneer Bhurji / Boiled Egg",
            "lunch": "Aloo Karela Bhaji, Lauki Kofta, Mix Dal, Curd / Kachumber, Plain Roti + Butter Roti, Chaas",
            "dinner": "Besan Gatte ki Sabji, Veg Fried Rice, Aloo Bhindi Bhaja, Dal Pancham, Water Melon Juice, Plain Roti + Butter Roti, Pickle"
        },
        "Friday": {
            "breakfast": "Idli + Masala Idli + Vada, Pav Bhaji, Watermelon, Egg Bhurji / Sweet Corn / Boiled Egg",
            "lunch": "Chilly Potato, Punjabi Chole, Dal Fry, Veg Biryani, Plain Roti + Butter Roti, Lemon Water, Curd / Veg Raita",
            "dinner": "Chicken Kasha / Shahi Paneer, Veg Pulav, Chana Daal, Rasmalai, Lemon Water, Plain Roti + Butter Roti, Methi Parantha"
        },
        "Saturday": {
            "breakfast": "Uttapam with Sambar & Chutney, Veg Cheese Sandwich, Banana, Egg Bhurji / Boiled Egg / Paneer Bhurji",
            "lunch": "Long Beans, Dum Aloo Kashmiri, Masoor Dal, Vegetable Khichdi, Plain Roti + Butter Roti, Lemon Water, Curd / Boondi Raita",
            "dinner": "Puri + Aloo Matar Green, Aloo Parwal Bhaji, Dal Tadka, Lemon Water, Plain Roti + Butter Roti"
        },
        "Sunday": {
            "breakfast": "Masala Dosa, Macroni / Masala Dalia, Pine Apple, Egg Bhurji / Boiled Egg / Paneer Bhurji",
            "lunch": "Cabbage Matar, Egg Curry / Malai Kofta Curry, Arhar Dal, Plain Roti + Butter Roti, Butter Milk, Curd / Boondi Raita",
            "dinner": "Chicken Butter Masala / Paneer Butter Masala, Masoor Dal, Veg Hyderabadi Biryani, Gulab Jamun, Lemon Water, Plain Roti + Butter Roti, Butter Naan"
        },
    },
    "Brahmaputra": {
        "Monday": {
            "breakfast": "Uthapam + Sambhar + Coconut Chutney, Veg Chowmein, Seasonal Fruits",
            "lunch": "Labra Masala (Dry), Rajma Masala, Dal Fry, Plain Rice, Sweet Lassi, Plain Roti/Ghee Roti, Curd, Papad",
            "dinner": "Lauki Chana (Dry), Aloo Matar Curry, Dhaba Dal Tadka, Tomato Rice/Plain Rice, Roohafza, Plain Roti/Ghee Roti"
        },
        "Tuesday": {
            "breakfast": "Poori Sabji, Jungli Sandwich, Seasonal Fruits",
            "lunch": "Mix Veg (Dry), Black Chana Curry, Arhar Dal Tadka, Jeera Rice/Plain Rice, Plain Roti/Ghee Roti, Curd, Watermelon Mint Cooler",
            "dinner": "Chole Bhature, Chatpate Aloo (Dry), Dal Tadka, Masala Lemonade, Plain Rice, Plain Roti/Ghee Roti, Fryums"
        },
        "Wednesday": {
            "breakfast": "Masala Idli + Sambhar + Coconut Chutney, Macroni Pasta, Seasonal Fruits",
            "lunch": "Aloo Parwal (Dry), Black Masoor Dal, Soya Keema Matar, Buttermilk, Plain Rice, Plain Roti/Ghee Roti, Curd, Peanut Papad",
            "dinner": "Butter Chicken / Paneer Butter Masala, Indian Fried Rice, Dal Makhni, Tandoor Roti, Rice Kheer/Pineapple Halwa, Tamarind Cooler, Roasted Papad"
        },
        "Thursday": {
            "breakfast": "Upma + Coconut Chutney, Kachori + Ghuguni, Seasonal Fruits",
            "lunch": "Mix Dal, Kadhi Pakora, Aloo Masala (Dry), Lemon Rice, Veg Raita, Plain Rice, Plain Roti/Ghee Roti, Curd, Papad",
            "dinner": "Lauki Kofta / Egg Curry, Lehsuni Chana Dal, Khatta Meetha Kaddu, Jaljeera, Plain Rice, Plain Roti/Ghee Roti"
        },
        "Friday": {
            "breakfast": "Pav Bhaji, Poha + Sev, Seasonal Fruits",
            "lunch": "Dhaba Dal Tadka, Nutrella Matar, Baingan Bharta, Watermelon Mint Cooler, Plain Rice/Curd Rice, Plain Roti/Ghee Roti, Curd",
            "dinner": "Matar Paneer / Chicken Kolhapuri, Dal Panch Mel, Onion Rice/Plain Rice, Kasuri Methi Paratha, Shahi Tukda, Masala Lemonade, Roasted Papad"
        },
        "Saturday": {
            "breakfast": "Aloo Pyaj Parantha + Curd + Chutney, Masala Dalia, Seasonal Fruits",
            "lunch": "Dal Makhani, Corn Masala, Esquash Masala, Masala Rice/Plain Rice, Roohafza, Plain Roti/Ghee Roti, Curd, Peanut Papad",
            "dinner": "Black Chana Masala (Dry), Lehsuni Chana Dal, Methi Matar Malai, Jaljeera Drink, Plain Rice, Plain Roti/Ghee Roti"
        },
        "Sunday": {
            "breakfast": "Masala Dosa + Sambhar + Coconut Chutney, Vermicelli Upma, Seasonal Fruits",
            "lunch": "Moong Masoor Dal, Aloo Chokha (Dry), Vatana Curry (White Peas), Chinese Fried Rice, Butter Milk, Plain Rice, Plain Roti/Ghee Roti, Curd, Fryums",
            "dinner": "Paneer Lababdar / Chicken Lababdar, Veg Dum Biriyani, Yellow Dal Tadka, Tamarind Cooler, Ice Cream, Butter Naan/Roti/Ghee Roti, Plain Rice, Roasted Papad"
        },
    },
    "Dhansiri": {
        "Monday": {
            "breakfast": "Veg Sandwich, Vegetable Uttappam (Carrot & Onion) + Sambar + Chutney, Fruits (Banana), Bread + Butter + Jam, Tea/Coffee/Milk, Egg / Paneer Bhurji / Egg Bhurji",
            "lunch": "Plain Rice, Chappati + Ghee Chappati, Masur Dal, Cabbage Sabji, Kadhi Pakoda, Salad + Pickle, Green Chutney, Curd / Onion Raita, Nimbu Pani + Sambhar, Fryums",
            "dinner": "Plain Rice, Chappati + Ghee/Butter Chappati, Black Chana Masala, Mix Veg, Arhar Dal, Salad + Pickle, Jaljeera Water, Rasam, Papad"
        },
        "Tuesday": {
            "breakfast": "Aloo Paratha + Curd + Chutney, Vermicelli Upma + Chutney, Fruits (Pineapple), Bread + Butter + Jam, Tea/Coffee/Milk, Sweet Corn / Paneer Bhurji",
            "lunch": "Plain Rice + Lemon Rice / Tamarind Rice (Alternate Weeks), Chappati + Ghee Chappati, Mix Dal, Lauki Sabji, Long Beans Sabji, Salad + Pickle, Black Sesame Chutney, Curd / Veg Raita, Chaas + Sambhar, Fryums",
            "dinner": "Plain Rice, Bhature + Chappati + Ghee/Butter Chappati, Masur Dal, Cholay Masala, Aloo Jeera Fry + Chilly Fry, Salad + Pickle, Nimbu Paani, Rasam, Papad"
        },
        "Wednesday": {
            "breakfast": "Pav Bhaji, Poha + Sev, Fruits (Pear), Bread + Butter + Jam, Tea/Coffee/Milk, Egg / Paneer Bhurji",
            "lunch": "Plain Rice, Chappati + Ghee Chappati, Moong Masur Dal, Red Pumpkin & Black Chana Sabji, Karela Fry, Salad + Pickle, Tomato Chutney, Curd / Boondi Raita, Lassi + Sambhar, Fryums",
            "dinner": "Plain Rice + Veg Biryani, Chappati + Ghee/Butter Chappati + Tandoori Butter Naan, Dal Tadka, Chicken Lababdar / Paneer Lababdar, Salad + Pickle, Rooh Afza, Ice Cream, Rasam, Papad"
        },
        "Thursday": {
            "breakfast": "Methi Paratha + Aloo chole sabji, Dahi + Sira + Gur, Fruits (Banana), Bread + Butter + Jam, Tea/Coffee/Milk, Sweet Corn / Paneer Bhurji",
            "lunch": "Plain Rice, Chappati + Ghee Chappati, Mix Dal, Mix Veg Dry, Alu Dum, Salad + Pickle, Mustard Green Chutney, Curd / Veg Raita, Chaas + Sambhar, Fryums",
            "dinner": "Plain Rice, Chappati + Ghee/Butter Chappati, Arhar Dal, Bhindi Aloo Fry, Rajma Curry, Salad + Pickle, Jaljeera Water, Rasam, Papad"
        },
        "Friday": {
            "breakfast": "Idli + Sambar + Chutney, Medu Vada + Sambar + Chutney, Fruits (Pineapple), Bread + Butter + Jam, Egg / Paneer Bhurji",
            "lunch": "Plain Rice + Khichdi, Chappati + Ghee Chappati, Masur Dal, Seasonable Vegetable, Raw Banana Fry, Salad + Pickle, Green Chutney, Curd / Onion Raita, Nimbu Pani + Sambhar, Fryums",
            "dinner": "Plain Rice + Veg Pulao, Chappati + Ghee/Butter Chappati, Mix Dal, Fish Curry / Kadhai Paneer / Mushroom Masala, Salad + Pickle, Nimbu Paani, Gulab Jamun, Rasam, Papad"
        },
        "Saturday": {
            "breakfast": "Ajwain Puri + Aloo Matar Sabji, Maggi, Fruits (Banana), Bread + Butter + Jam, Sweet Corn / Paneer Bhurji",
            "lunch": "Plain Rice, Chappati + Ghee Chappati, Chana Dal, Soyabean Masala, Baingan Bharta, Salad + Pickle, Lehsun Onion Chutney, Curd / Raita, Sweet Lassi + Sambhar, Fryums",
            "dinner": "Plain Rice, Chappati + Ghee/Butter Chappati, Mix Dal, Malai Kofta / Egg Curry, Aloo Pitika Choka, Salad + Pickle, Rooh Afza, Rasam, Papad"
        },
        "Sunday": {
            "breakfast": "Mysore Masala Dosa + Sambar + Chutney, Sweet Dalia, Fruits (Watermelon), Bread + Butter + Jam, Egg / Paneer Bhurji",
            "lunch": "Plain Rice + Veg fried rice, Chappati + Ghee Chappati, Arhar Dal, Mix vegetable, Manchurian Gravy, Salad + Pickle, Tomato Chutney, Curd / Raita, Chaas + Sambhar, Fryums",
            "dinner": "Plain Rice + Veg Pulav, Garlic Tandoori Butter Naan + Chappati + Ghee/Butter Chappati, Dal Makhani, Handi Chicken/Handi Paneer, Rasgulla, Salad + Pickle, Jaljeera Water, Rasam, Papad"
        },
    },
    "Dihing": {
        "Monday": {
            "breakfast": "Besan Chilla, Upma with Ground Chutney, Fruits",
            "lunch": "Aloo Dum, Cabbage Matar, Arhar Dal, Kashmiri Pulao, Plain Rice, Chapati (Butter+Plain), Papad, Chutney, Curd, Rasna, Sambhar, Green Salad",
            "dinner": "Egg Curry / Malai Kofta, Aloo Long Beans Fry, Dal Tadka, Rasam, Chapati (Butter+Plain), Fryums, Green Salad, Neembu Paani, Plain Rice"
        },
        "Tuesday": {
            "breakfast": "Aloo Paratha, Dahi + Chira + Gud, Fruits",
            "lunch": "Kundru with Black Chana, Rajma Masala, Chana Dal, Plain Rice, Chapati (Butter+Plain), Papad, Chutney, Curd, Butter Milk, Sambhar, Green Salad",
            "dinner": "Bhindi Masala, Chilli Soyabean, Moong Daal, Plain Rice, Chapati (Butter+Plain), Fryums, Neembu Paani, Rasam, Green Salad"
        },
        "Wednesday": {
            "breakfast": "Uttappam, Vada Pav, Sambhar + Coconut Chutney, Fruits",
            "lunch": "Aloo Karela Fry, Lauki Chana, Masoor Dal, Plain Rice, Chapati (Butter+Plain), Papad, Chutney, Curd, Butter Milk, Sambhar, Green Salad",
            "dinner": "Rajasthani Chicken / Rajasthani Paneer, Dal Makhani, Tandoori Roti, Veg Biryani, Fryums, Gulab Jamun, Neembu Paani, Green Salad, Rasam"
        },
        "Thursday": {
            "breakfast": "Idli (Boiled + Masala) + Medhu Wada, Chowmein, Fruits",
            "lunch": "Chana Dal, Rajma Masala, Baigan Aloo Sabji, Jeera Rice, Plain Rice, Roti (Plain+Butter), Sambhar, Curd, Jaljeera, Chatni, Roasted Papad, Salad",
            "dinner": "Mix Dal, Chole Masala, Aloo Jeera, Bhature, Plain Rice, Chapati, Rasam, Green Salad, Neembu Paani, Fried Chilli, Imli Chutney, Lachha Pyaz"
        },
        "Friday": {
            "breakfast": "Kachori with Ghughni, Poha with Bhujia, Fruits",
            "lunch": "Bhindi Masala, Black Chana, Masoor Dal, Plain Rice, Roti (Plain+Butter), Sambhar, Curd, Rasna, Chatni, Fryums, Salad",
            "dinner": "Fish Curry, Butter Paneer Masala, Dal Fry, Peas Pulao, Plain Rice, Chapati (Plain/Butter), Rasam, Pineapple Halwa, Neembu Paani, Green Salad"
        },
        "Saturday": {
            "breakfast": "Aloo Onion Paratha, Fried Pasta, Fruits",
            "lunch": "Dal Khichdi, Aloo Chokha, Moong Dal, Labra Sabzi, Plain Rice, Roti (Plain+Butter), Sambhar, Curd, Jaljeera, Chatni, Fried Papad, Salad",
            "dinner": "Black Chana Masala, Aloo Parwal, Chana Dal, Plain Rice, Chapati (Butter/Normal), Fryums, Neembu Paani, Green Salad, Rasam"
        },
        "Sunday": {
            "breakfast": "Masala Dosa, Sambhar + Coconut Chutney, Sweet Daliya, Fruits",
            "lunch": "Kadhi Pakora, Dal Tadka, Spine Guard, Lemon Rice, Plain Rice, Chapati (Plain + Butter), Sambhar, Curd, Lassi, Chatni, Roasted Papad, Salad",
            "dinner": "Paneer Lababdar, Chicken Lababdar, Dal Makhani, Butter Naan, Masala Rice, Ice Cream, Fryums, Green Salad, Rasam, Neembu Paani"
        },
    },
    "Disang": {
        "Monday": {
            "breakfast": "Veg Fried Maggi, Besan Chilla, Green Chutney, Fruits",
            "lunch": "Aloo Dum, Cabbage Matar, Arhar Dal, Kashmiri Pulao, Plain Rice, Chapati (Butter + Plain), Papad, Theccha, Curd, Lassi, Sambhar, Green Salad",
            "dinner": "Plain Rice, Mix Dal, Chole Masala, Aloo Jeera, Rasam, Bhature, Chapati, Green Salad, Lemon Water"
        },
        "Tuesday": {
            "breakfast": "Idli (Boiled + Masala) + Medhu Vada, Coconut Chutney + Sambhar, Dahi + Chira + Gud, Fruits",
            "lunch": "Aloo Karela Fry, Lauki Chana, Masoor Dal, Plain Rice, Chapati (Butter + Plain), Papad, Lehsun Chutney, Curd, Butter Milk, Sambhar, Green Salad",
            "dinner": "Egg Curry / Lauki Kofta, Aloo Long Beans Fry, Dal Tadka, Rasam, Chapati (Butter + Plain), Fryums, Green Salad, Lemon Water, Plain Rice"
        },
        "Wednesday": {
            "breakfast": "Masala Dosa, Fried Pasta, Sambhar + Coconut Chutney, Fruits",
            "lunch": "Tendli (Kundru), Lobia Masala, Plain Rice, Chana Dal, Chapati (Butter + Plain), Papad, Pineapple Chutney, Curd, Butter Milk, Sambhar, Green Salad",
            "dinner": "Rajasthani Chicken / Kadai Paneer, Dal Makhani, Tandoori Roti, Veg Biryani, Fryums, Rasmalai, Rasna, Green Salad, Rasam"
        },
        "Thursday": {
            "breakfast": "Aloo Onion Paratha, Curd, Green Chutney, Poha with Usal, Fruits",
            "lunch": "Jeera Rice, Plain Rice, Arhar Dal, Rajma Masala, Baigan Bharta, Roti (Plain + Butter), Sambhar, Curd, Lassi, Mustard Chutney, Roasted Papad, Salad",
            "dinner": "Pumpkin Chana, Aloo Matar Tomato, Moong Dal, Plain Rice, Chapati (Butter + Plain), Fryums, Jaljeera, Rasam, Green Salad"
        },
        "Friday": {
            "breakfast": "Pav Bhaji, Chowmein, Fruits",
            "lunch": "Aloo Bhindi Fry, Black Chana, Masoor Dal, Roti (Plain + Butter), Sambhar, Curd, Veg Raita, Dhaniya Pudina Chutney, Fryums, Salad, Plain Rice",
            "dinner": "Plain Paratha, Chapati, Dal Fry, Rasam, Fish Curry, Butter Paneer Masala / Mushroom Masala, Chapati (Plain / Butter), Gulabjamun, Jaljeera, Green Salad"
        },
        "Saturday": {
            "breakfast": "Kachori with Ghughni, Upma with Groundnut Chutney, Fruits",
            "lunch": "Dal Khichdi, Aloo Chokha, Moong Dal, Labra Sabji, Curd, Bundi Raita, Spicy Tomato Coriander Roasted Chutney, Fried Papad, Salad, Plain Rice, Roti (Plain + Butter)",
            "dinner": "Veg Manchurian, Aloo Parwal, Plain Rice, Chapati (Butter / Normal), Chana Dal, Fryums, Rooh-af-ja, Green Salad, Rasam"
        },
        "Sunday": {
            "breakfast": "Mysore Masala Dosa, Sambhar, Coconut Chutney, Masala Oats / Sweet Daliya, Fruit",
            "lunch": "Kadhi Pakora, Lemon Rice, Dal Tadka, Spine Guard + Aloo with Posto, Sambhar, Curd, Dahi Vada, Imli Chutney, Roasted Papad, Salad, Plain Rice, Roti (Plain + Butter)",
            "dinner": "Rajasthani Paneer, Kadai Chicken, Butter Naan, Dal Makhani, Masala Rice, Ice Cream, Fryums, Green Salad, Rasam, Nimbu Paani"
        },
    },
    "Gaurang": {
        "Monday": {
            "breakfast": "Puri + Aloo Matar Sabji, Sev - Poha, Seasonal Fruit",
            "lunch": "Kadhi Pakora, Cabbage Green Peas, Mix Daal Fry, Plain Rice + Lemon Rice, Butter Roti & Plain Roti, Curd, Lassi, Chutney",
            "dinner": "Egg Curry / Veg Kofta, Lauki Chana, Arhar Daal Tarka, Plain Rice, Butter Roti + Plain Roti, Nimbu Pani, Chutney"
        },
        "Tuesday": {
            "breakfast": "Besan Chila / Moong Dal Chila, Daliya, Seasonal Fruit, Emli Chutney",
            "lunch": "Patal Aloo Fry, Black Chana Masala, Masoor Daal, Plain Rice, Butter Roti + Plain Roti, Nimbu Pani, Curd, Chutney",
            "dinner": "Long Bean, Aloo Soyabean, Chana Dal Fry, Plain Rice, Plain Roti, Jal Jeera, Chutney"
        },
        "Wednesday": {
            "breakfast": "Uttapam + Sambar + Chutney, Chowmein / Vada Pav, Seasonal Fruit",
            "lunch": "Chole Bhature, Pumpkin Masala, Black Dal, Plain Rice, Butter Roti / Plain Roti, Chaas, Curd, Chutney",
            "dinner": "Kadai Chicken / Kadai Paneer, Tawa Naan & Plain Roti, Arhar Dal Fry, Veg Pulao & Plain Rice, Green Chutney, Ice Cream, Boondi Raita"
        },
        "Thursday": {
            "breakfast": "Plain Idli + Vada + Chutney + Sambhar, Daliya Namkeen, Seasonal Fruit",
            "lunch": "Rajma Masala, Bhatt Karela, Masoor Dal, Plain Rice + Jeera Rice, Butter Roti / Plain Roti, Nimbu Pani, Curd, Chutney",
            "dinner": "Ghughni, Aloo Jeera, Chana Dal Fry, Plain Rice, Plain Roti + Puri, Jal Jeera, Chutney"
        },
        "Friday": {
            "breakfast": "Pav Bhaji, Veg Pasta / Upma, Seasonal Fruit",
            "lunch": "Torai, Raw Banana Sabji, Mix Daal, Plain Rice, Butter Roti / Plain Roti, Green Chutney, Curd, Lassi",
            "dinner": "Matar Paneer / Fish Curry, Moong Masoor Dal, Plain Rice + Jeera Rice, Butter Roti / Plain Roti, Shahi Tukra / Sooji Halwa, Nimbu Pani, Chutney"
        },
        "Saturday": {
            "breakfast": "Aloo Paratha, Dahi Chira Gur, Seasonal Fruit",
            "lunch": "Mix Chokha, Khichdi, Arhar Daal Tarka, Plain Rice, Butter Roti / Plain Roti, Curd, Nimbu Pani, Chutney",
            "dinner": "Manchurian, Bhindi Aloo, Moong Daal, Plain Rice + Fried Rice, Butter Roti / Plain Roti, Jal Jeera, Chutney"
        },
        "Sunday": {
            "breakfast": "Masala Dosa + Coconut Chutney + Sambar, Veg Sandwich, Seasonal Fruit",
            "lunch": "Escauce, Sev Tomato, Mix Dal, Plain Rice, Butter Roti / Plain Roti, Curd, Chaas, Green Chutney",
            "dinner": "Chicken Butter Masala / Paneer Butter Masala, Methi Parantha, Dal Makhani, Veg Biriyani + Plain Rice, Butter Roti / Plain Roti, Gulab Jamun, Veg Raita, Chutney"
        },
    },
    "Kameng": {
        "Monday": {
            "breakfast": "Puri + Ghugni, Suji Upma, Egg (Boiled/Bhurji), Paneer Bhurji, Seasonal Fruit",
            "lunch": "Tawa Veg (Dry), Black chana/Rajma, Dal fry, Vegetable Rice, Curd",
            "dinner": "Veg Kofta / Egg curry, Alo pata gobi matar, Chana Dal fry, Rice, Roti"
        },
        "Tuesday": {
            "breakfast": "Aloo/Onion Paratha, Veg Chowmein, Seasonal Fruits",
            "lunch": "Aloo Parawal sabji, Aloo karal fry, Fried Rice, Mix Dal, Curd",
            "dinner": "Chole Bhatura, Jeera Alu fry, Chana dal, Rice"
        },
        "Wednesday": {
            "breakfast": "Uthappam, Veg Sandwich, Sweet corn, Egg (Boiled/Bhurji), Banana",
            "lunch": "Bhindi masala, Curry pakora, Toor Dal, Jeera Rice, Curd",
            "dinner": "Kadhai Chicken / Kadhai Paneer, Fried Rice, Gulab Jamun, Butter Naan, Toor Dal"
        },
        "Thursday": {
            "breakfast": "Plain Paratha + Alu Sabji, Dhai Chira, Seasonal Fruits",
            "lunch": "Mix Veg, Aloo Soyabean, Arhar Dal, Veg Pulao, Curd",
            "dinner": "Veg Navaratna curry, Aloo kundi fry, Mung Daal with gajar and peas"
        },
        "Friday": {
            "breakfast": "Idli + Vada, Pav Bhaji, Egg (Boiled/bhurji), Sweet Corn, Seasonal Fruits",
            "lunch": "Aloo Beams, Lokki Chana, Curd",
            "dinner": "Chicken Curry / Matar Paneer, Peas Pulao, Laccha Paratha, Masoor Dal"
        },
        "Saturday": {
            "breakfast": "Kachori + Ghuguni, Poha + Sev Bhujiya, Banana, Egg (Boiled/Bhurji), Panner Bhurji, Curd",
            "lunch": "Labra Veg, Aloo Chokha, Khichdi, Curd/Raita",
            "dinner": "Aloo Beams, Torai, Dal makhani"
        },
        "Sunday": {
            "breakfast": "Masala Dosa / Mysore Masala Dosa, Sweet Dalia, Seasonal Fruits, Egg (Boiled / Bhurji), Paneer Bhurji / Sweet Corn",
            "lunch": "Puri, Dum Aloo, Pumpkin Chana, Moong Masoor Dal, Curd",
            "dinner": "Chicken Butter Masala / Paneer Butter Masala, Hyderabadi Veg Biryani, Raita, Tandoori Roti, Arhar Dal, Ice cream"
        },
    },
    "Kapili": {
        "Monday": {
            "breakfast": "Puri + Ghoogni, Suji Upma, Egg (Boiled/Bhurji), Paneer Bhurji, Pineapple",
            "lunch": "Chole Pyaaz Sabji (Dry), Lauki Kofta, Chana Dal, Vegetable Rice, Curd, Masala Chaas",
            "dinner": "Chilli Soya Bean, Tawa Veg, Mix Dal, Tomato Rice, Nimbu Paani"
        },
        "Tuesday": {
            "breakfast": "Poha + Sev Bhujia, Veg Roll, Egg (Boiled/Bhurji), Paneer Bhurji, Seasonal Fruit",
            "lunch": "Aloo Cabbage-Mater, Veg Manchurian, Fried Rice, Moong-Masoor Dal, Curd, Nimbu Paani",
            "dinner": "Rajma Masala, Pumpkin Chana, Chana Dal, Savory Rice, Jaljeera"
        },
        "Wednesday": {
            "breakfast": "Onion Uttapam, Fried Maggi, Egg (Boiled/Bhurji), Sweet Corn, Banana",
            "lunch": "Besan Gatta, Aloo Bhindi Masala, Toor Dal, Lemon Rice, Boondi Raita, Meethi Chaas",
            "dinner": "Kadhai Chicken / Kadhai Paneer, Vegetable Rice, Gulab Jamun, Butter Naan, Mix Daal, Rasna"
        },
        "Thursday": {
            "breakfast": "Besan Chilla, Veg Sandwich, Egg (Boiled/Bhurji), Paneer Bhurji, Pineapple",
            "lunch": "Dry Karela Aloo, Aloo Baingan Masala, Arhar Dal, Veg Pulao, Curd, Nimbu Paani",
            "dinner": "Chole Masala + Bhature, Long Bean Aloo, Chana Dal, Lassi, Jeera Rice"
        },
        "Friday": {
            "breakfast": "Idli + Vada, Pav Bhaji, Egg (Boiled/Bhurji), Sweet Corn, Seasonal Fruit",
            "lunch": "Kadhi Pakora, Jeera Aloo, Lobia Masala, Lemon Rice, Curd, Masala Chaas",
            "dinner": "Matar Paneer / Chicken Kosha, Peas Pulao, Paratha, Masoor Dal, Fruit Custard, Jaljeera"
        },
        "Saturday": {
            "breakfast": "Aloo + Onion Paratha, White Pasta, Egg (Boiled/Bhurji), Paneer Bhurji, Banana, Curd",
            "lunch": "Dum Aloo, Labra Veg, Tomato Rice, Mix Dal, Dahi Vada, RoohAfza",
            "dinner": "Egg Curry / Malai Kofta, Chana Dal Fry, Rice Kheer, Dal Makhani, Nimbu Paani"
        },
        "Sunday": {
            "breakfast": "Mysore Masala Dosa, Sweet Dalia, Egg (Boiled/Bhurji), Sweet Corn, Seasonal Fruit",
            "lunch": "Aloo / Baingan Bharta, Mixed Veg, Khichdi, Moong-Masoor Dal, Vegetable Raita, Nimbu Paani",
            "dinner": "Paneer Butter Masala / Chicken Butter Masala, Hyderabadi Dum Biryani, Onion Raita, Tandoori Roti, Ice Cream, Arhar Dal, RoohAfza"
        },
    },
    "Lohit": {
        "Monday": {
            "breakfast": "Veg Fried Maggi, Besan Chilla + Green Chutney, Fruits",
            "lunch": "Mix Veg, Rajma Masala, Masoor Daal, Peas Pulao, Roti, Veg Raita, Curd, Chutney",
            "dinner": "Veg Kofta / Egg Curry, Lowki Channa Sabji, Dal Fry, Rice, Roti, Nimbu Pani, Chutney"
        },
        "Tuesday": {
            "breakfast": "Idly + Masala Idly + Vada, Samber, Chutney, Fried Pasta, Fruits",
            "lunch": "Dum Aloo, Aloo + Cabbage + Matar, Arhar Dal, Rice, Roti, Curd, Lassi, Chutney",
            "dinner": "Masala Chole, Aloo Jeera, Chana Dal, Bhature + Chapati, Rice, Jaljeera, Chutney"
        },
        "Wednesday": {
            "breakfast": "Aloo Onion Paratha, Green Chutney, Curd, Dahi Chera, Gur, Fruits",
            "lunch": "Long Beans Sabzi, Black Channa Masala, Mix Dal, Jeera Rice, Roti, Curd, Chutney, Neembu Pani",
            "dinner": "Chicken Kolhapuri / Paneer Kolhapuri, Veg Biryani, Dal Makhni, Tawa Paratha / Roti, Veg Raita, Rabdi Jalebi, Chutney"
        },
        "Thursday": {
            "breakfast": "Pav Bhaji, Vegetable Upma + Coconut Chutney, Fruits",
            "lunch": "Aloo Parwal Sabji, Tamatar Sev, Dal Makhani, Rice, Roti, Curd, Butter Milk, Chutney",
            "dinner": "Tendly Channa, Aloo Soyabean, Dal Tadka, Rice, Roti, Neembu Pani, Chutney"
        },
        "Friday": {
            "breakfast": "Onion Utthapam + Samber + Chutney, Veg Chowmein + Tomato Sauce, Fruits",
            "lunch": "Aloo Brinjal, Besan Gatta, Moong Daal, Rice, Roti, Curd, Sweet Lassi, Chutney",
            "dinner": "Chicken Lababdar / Paneer Lababdar, Masala Rice, Dal Fry, Roti, Jaljeera, Gulab Jamun, Chutney"
        },
        "Saturday": {
            "breakfast": "Kachori + Ghuguni + Imli Chutney, Poha + Sev Bhujiya, Fruits",
            "lunch": "Labra Sabzi, Aloo Chokha, Chana Dal, Khichdi, Roti, Curd, Veg Raita, Chutney",
            "dinner": "Mix Veg Sabji, Black Channa Masala, Arhar Dal, Rice, Roti, Nimbu Pani, Chutney"
        },
        "Sunday": {
            "breakfast": "Mysore Masala Dosa + Coconut Chutney + Sambar, Sweet Dalya, Fruits",
            "lunch": "Kadhi Pakoda, Aloo + Bhindi Masala, Arhar Dal, Lemon Rice, Roti, Curd, Boondi Raita, Chutney",
            "dinner": "Chicken Butter Masala / Paneer Butter Masala, Dal Makhani, Peas Pulao, Tandoori Butter Naan / Roti, Jaljeera, Rasmalai / Ice Cream, Chutney"
        },
    },
    "Manas": {
        "Monday": {
            "breakfast": "Aloo Onion Paratha & Dahi, Daliya, Banana, Corn / Boiled Egg / Egg Bhurji",
            "lunch": "Rajma Masala & Aloo Soya Masala, Rice & Dal Fry, Veg Pulao & Rasam, Tamarind Chutney + Raita & Lassi, Salad + Pickle + Papad",
            "dinner": "Paneer Malai Kofta / Egg Masala, Rice & Dal Fry, Rasam & Mint Chutney, Jal Jeera Paani, Salad + Pickle"
        },
        "Tuesday": {
            "breakfast": "Dosa & Sevay Upma (Vermicelli), Watermelon, Paneer Bhurji / Boiled Egg / Egg Bhurji",
            "lunch": "Black Chana Masala & Aloo Padwal, Rice & Masoor Dal, Rasam / Sambhar, Garlic Chutney + Dahi & Nimbu Pani, Salad + Pickle + Fryums",
            "dinner": "Chole Bhature & Aloo Jeera, Rice & Lehsuni Dal Tadka, Rasam & Dhaniya Chutney, Nimbu Pani, Salad + Pickle"
        },
        "Wednesday": {
            "breakfast": "Pav Bhaji & Poha, Banana, Corn / Boiled Egg / Egg Bhurji",
            "lunch": "Lauki Kofta & Veg Khorma, Rice & Moong Dal, Sambhar & Tamarind Rice, Mint Chutney + Dahi & Lassi, Salad + Pickle + Papad",
            "dinner": "Paneer Butter Masala / Chicken Kadhai, Roti & Rice, Arhar Dal Tadka & Rasam, Veg Dum Biryani & Garlic Chutney, Jal Jeera Paani & Gulab Jamun, Salad + Pickle"
        },
        "Thursday": {
            "breakfast": "Idli (Plain + Masala) & Medu Vada, Naspati (Fruit), Paneer Bhurji / Boiled Egg / Egg Bhurji",
            "lunch": "Sprout Masala & Aloo Beans, Rice & Arhar Dal Tadka, Sambhar & Tamarind Chutney, Dahi & Chaas, Salad + Pickle + Fryums",
            "dinner": "Dahi Bhindi & Aloo Cabbage Matar, Rice & Dal Fry, Rasam & Mint Chutney, Nimbu Paani, Salad + Pickle"
        },
        "Friday": {
            "breakfast": "Piyaz Kachori & Veg Fried Maggi, Mint Chutney & Mint Yoghurt Dip, Guava, Corn / Boiled Egg / Egg Bhurji",
            "lunch": "Chole Masala & Brinjal Tomato Pitika, Rice + Dal + Sambhar, Tomato Chutney + Dahi & Lassi, Salad + Pickle + Fryums",
            "dinner": "Paneer Lababdar / Butter Chicken, Rice & Methi Paratha, Mix Dal Fry & Rasam, Veg Pulao & Garlic Chutney, Jal Jeera Paani & Fruit Custard, Salad + Pickle"
        },
        "Saturday": {
            "breakfast": "Dhokla & Upma, Banana, Corn / Boiled Egg / Egg Bhurji",
            "lunch": "Labra Sabji & Aloo Bhindi, Rice & Arhar Dal, Khichdi + Sambhar + Mint Chutney, Dahi & Chaas, Salad + Pickle + Papad",
            "dinner": "Lobia Masala & Kashmiri Dum Aloo, Rice & Dal Makhani, Rasam & Mint Chutney, Nimbu Paani, Salad + Pickle"
        },
        "Sunday": {
            "breakfast": "Karam Masala Dosa & Pasta, Sambhar & Coconut Chutney, Pineapple, Paneer Bhurji / Boiled Egg / Egg Bhurji",
            "lunch": "Kadhi Pakoda & Tawa Veg, Rice & Lehsuni Dal Tadka, Rasam & Tamarind Chutney, Dahi & Nimbu Pani, Salad + Pickle + Fryums",
            "dinner": "Paneer Do Pyaaza / Chicken Kolhapuri, Garlic Naan & Rice, Chana Dal & Rasam, Veg Pulao & Garlic Chutney, Nimbu Pani & Ice-Cream, Salad + Pickle"
        },
    },
    "Siang": {
        "Monday": {
            "breakfast": "Idli, Idli Masala, Pav Bhaji, Watermelon, Plain / Butter Roti, Boondi Raita / Curd, Lassi, Papad",
            "lunch": "Plain Rice, Kadhi Pakoda, Moong Dal, Imli Chutney, Aloo Bhindi Masala, Jaljeera, Green Chutney, Papad",
            "dinner": "Plain Rice, Egg Curry, Veg Malai Kofta, Mix Dal, Plain / Butter Roti"
        },
        "Tuesday": {
            "breakfast": "Aloo Pyaaz Paratha, Vermicelli Upma, Dahi, Pineapple",
            "lunch": "Black Eyed Beans, Beans Aloo Dry, Arhar Dal, Plain Rice, Butter / Plain Roti, Tomato Chutney, Chaas, Curd / Raita, Papad",
            "dinner": "Plain Rice, Methi Matar Malai, Urad Dal, Chilli Soya Dry, Plain / Butter Roti, Nimbu Pani, Imli Chutney, Papad"
        },
        "Wednesday": {
            "breakfast": "Kachori + Ghugni, Poha, Banana",
            "lunch": "Plain Rice, Dry Pumpkin, Amritsari Chole, Dal, Plain / Butter Roti, Curd / Raita, Lassi, Dhaniya Chutney, Papad",
            "dinner": "Paneer Butter Masala, Chicken Butter Masala, Dal Fry, Veg Biryani, Naan, Gulab Jamun, Raita, Plain / Jeera Rice"
        },
        "Thursday": {
            "breakfast": "Masala Dosa, Chowmein, Pineapple",
            "lunch": "Rajma, Plain Rice, Fried Rice, Aloo Brinjal Pitika, Moong Dal, Plain / Butter Roti, Curd / Raita, Chaas, Papad",
            "dinner": "Plain Rice, White Peas Masala Curry, Honey Chilli Potato, Dal Fry, Plain / Butter Roti, Jaljeera, Papad"
        },
        "Friday": {
            "breakfast": "Pasta, Stuffed Dal Paratha + Green Chutney, Banana",
            "lunch": "Kashmiri Pulao, Kala Chana Masala, Plain Rice, Aloo Jeera, Arhar Dal, Raita / Curd, Green Chutney, Plain / Butter Roti, Nimbu Paani",
            "dinner": "Afgani Paneer, Afgani Chicken, Dal Kolhapuri, Veg Pulao, Plain Rice, Plain / Butter Roti, Rabdi Jalebi, Nimbu Paani"
        },
        "Saturday": {
            "breakfast": "Upma, Uttapam, Watermelon",
            "lunch": "Soyabean Gravy, Veg Manchurian, Plain / Butter Roti, Dal, Plain Rice, Curd / Raita, Lassi, Fried Rice, Papad",
            "dinner": "Plain Rice, Chole Gravy, Gobhi Matar, Plain Roti / Bhature, Dal Tadka, Nimbu Paani, Groundnut Chutney, Papad"
        },
        "Sunday": {
            "breakfast": "Karam Masala Dosa, Sweet Daliya, Banana",
            "lunch": "Plain Rice, Papaya Khaar / Besan Gatta, Veg Tawa, Dal Fry, Plain / Butter Roti, Curd / Raita, Chaas, Imli Chutney, Khichdi",
            "dinner": "Paneer Lababdar, Chicken Kolhapuri, Tandoori Roti, Dal Makhani, Veg Dum Biryani, Plain / Butter Roti, Ice Cream, Raita"
        },
    },
    "Umiam": {
        "Monday": {
            "breakfast": "Idli (Plain + Masala) + Sambar & Coconut Chutney, Medu Vada, Banana, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn",
            "lunch": "Baingan ka Bharta, Rajma Masala, Masoor Daal, Plain Rice / Jeera Rice, Roti / Butter Roti, Chaas, Curd, Pudeena Chutney, Papad, Salad",
            "dinner": "Egg Curry / Veg Kofta Curry, Dry Patal sabji, Dal Tadka, Plain Rice, Roti / Butter Roti, Chutney, Nimbu Pani + Salad, Papad"
        },
        "Tuesday": {
            "breakfast": "Aloo Onion Paratha + Chutney + Curd, Veg Fried Pasta, Pineapple, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn",
            "lunch": "Aloo Bhindi Masala, Lobia Masala, Moong Masoor Dal, Kashmiri Pulao / Plain Rice, Roti / Butter Roti, Curd, Lassi, Schezwan Tomato Chutney, Papad",
            "dinner": "Masala Chole, Aloo Jeera, Chana Dal, Bhature + Chapati, Plain Rice, Jaljeera, Chutney, Salad, Papad"
        },
        "Wednesday": {
            "breakfast": "Veg Uttappam with Sambhar and Coconut Chutney, Pav Bhaji, Banana, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn",
            "lunch": "Dum Aloo, Cabbage Matar, Arhar Dal, Plain Rice, Roti, Curd, Veg Raita, Chutney, Papad",
            "dinner": "Chicken Kosha / Boiled Chicken + Paneer Kosha, Dal Makhni, Gulab Jamun, Plain Rice / Veg Pulao, Methi Paratha, Nimbu Pani, Chutney, Salad, Papad"
        },
        "Thursday": {
            "breakfast": "Puri + Aloo Matar Sabji, Poha, Watermelon, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn",
            "lunch": "Aloo Karela, Soyabean Curry, Chana Dal, Jeera Rice, Roti, Curd, Chutney, Butter Milk, Papad",
            "dinner": "Aloo Long Beans, Rajma Masala, Dal Tadka, Plain Rice, Roti / Butter Roti, Chutney, Nimbu Pani, Salad, Papad"
        },
        "Friday": {
            "breakfast": "Kachori Aloo Onion + Ghughani, Upma, Pineapple, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn",
            "lunch": "Mix Veg, Black Chana Masala, Masoor Dal, Rice, Roti, Curd, Sweet Lassi, Chutney, Papad",
            "dinner": "Kadhai Chicken / Kadhai Paneer, Green Moong Dal, Peas Pulao / Plain Rice, Roti / Lachha Paratha, Rooh Afza, Rasmalai / Jalebi with Rabadi, Chutney, Salad"
        },
        "Saturday": {
            "breakfast": "Masala Dosa + Coconut Chutney + Sambar, Masala Oats / Sweet Dalia, Banana, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn, Mysore Chutney",
            "lunch": "Lauki Sabzi, Aloo Chokha, Moong Masoor Dal, Khichdi, Plain Rice, Roti, Curd, Boondi Raita, Chutney, Papad",
            "dinner": "Veg Manchurian, Bhindi Masala, Arhar Daal, Rice + Fried Rice, Roti, Nimbu Pani, Chutney, Salad, Papad"
        },
        "Sunday": {
            "breakfast": "Aloo Paratha + Curd, Chowmein, Banana, Egg Bhurji / Boiled Egg / Paneer Bhurji / Sweet Corn",
            "lunch": "Amritsari Chhola Masala, Dal Maharani, Lemon Rice, Puri / Roti, Dahi Vada + Imli Chutney, Salad, Papad",
            "dinner": "Butter Chicken Masala / Paneer Masala, Hyderabadi Veg Biriyani / Plain Rice, Arhar Dal, Tandoori Roti / Plain Roti, Boondi Raita, Ice Cream, Nimbu Pani, Salad"
        },
    },
    "Subansiri": {
        "Monday": {
            "breakfast": "Idli + Fried Idli / Medu Vada, Sambar Chutney, Veg Fried Maggie, Boiled Egg / Egg Bhurji / Paneer Bhurji, Banana",
            "lunch": "Plain Rice / Tomato Rice, Masoor Dal + Rasam, Black Chana Curry, Aloo Cabbage Fry, Roti / Butter Roti, Curd, Salad, Chaas, Pudina Chutney, Papad",
            "dinner": "Plain Rice, Chana Dal + Sambhar, Aloo Jeera, Veg Manchurian, Roti / Butter Roti, Salad, Nimbu Pani, Papad, Tomato Chutney"
        },
        "Tuesday": {
            "breakfast": "Poha Bhujia, Pav Bhaji, Boiled Egg / Egg Bhurji / Boiled Corn, Watermelon",
            "lunch": "Plain Rice, Moong Dal + Rasam, Mix Saag Bhaji, Bhindi Masala, Roti / Butter Roti, Curd, Salad, Lassi, Papaya Khar, Papad",
            "dinner": "Plain Rice, Bhature, Mix Dal + Rasam, Raw Banana Fry, Masala Chole, Roti / Butter Roti, Salad, Nimbu Pani, Papad, Garlic Chutney"
        },
        "Wednesday": {
            "breakfast": "Masala Dosa, Sambar, Coconut Chutney, Daliya Khichdi, Banana, Boiled Egg / Egg Bhurji / Paneer Bhurji",
            "lunch": "Plain Rice, Urad Dal + Sambhar, Rajma Masala, Brinjal Aloo Pitika, Roti / Butter Roti, Curd, Salad, Chaas, Tomato Chutney, Papad",
            "dinner": "Veg Pulao / Plain Rice, Dal Lasooni (Moong) + Sambhar, Matar Paneer / Chicken Kosha / Boiled Chicken, Roti / Naan, Gulab Jamun, Salad, Nimbu Pani, Papad, Pudina Chutney"
        },
        "Thursday": {
            "breakfast": "Ajwain Puri + Ghugni, Suji Upma, Coconut Chutney, Pineapple / Plum, Boiled Egg / Egg Bhurji / Boiled Corn",
            "lunch": "Plain Rice / Jeera Rice, Otenga Dal + Rasam, Tawa Veg, Kadhi, Roti / Butter Roti, Curd, Salad, Lassi, Garlic Chutney, Papad",
            "dinner": "Plain Rice, Arhar Dal + Rasam, Aloo Soybean Curry, Beans Gajar Fry, Roti / Butter Roti, Salad, Nimbu Pani, Papad, Masoor Daal Chutney"
        },
        "Friday": {
            "breakfast": "Vegetable Uttapam, Sambar Coconut Chutney, Vermicelli Upma, Guava / Watermelon, Boiled Egg / Egg Bhurji / Paneer Bhurji",
            "lunch": "Plain Rice, Whole Masoor Dal + Sambhar, Lauki Kofta Curry, Aloo Long Beans Fry, Roti / Butter Roti, Raita, Curd, Salad, Chaas, Chilli and Garlic Chutney, Papad",
            "dinner": "Vegetable Fried Rice / Plain Rice, Moong Dal with Gajar and Peas + Rasam, Chilli Paneer / Chilli Mushroom / Fish Curry, Roti / Butter Roti / Lachha Paratha, Fruit Custard, Salad, Nimbu Pani, Papad, Mustard and Chilli Chutney"
        },
        "Saturday": {
            "breakfast": "Aloo Paratha / Dal Paratha, Dahi Chira, Tomato Coriander Chutney, Pear, Boiled Egg / Egg Bhurji / Boiled Corn",
            "lunch": "Plain Rice / Khichdi, Dal Fry + Rasam, Small Potato Fry, Labra Sabji, Roti / Butter Roti, Curd, Salad, Lassi, Coriander Chutney, Papad",
            "dinner": "Plain Rice, Dal Makhani + Rasam, Egg Curry / Veg Kofta Curry, Pumpkin Chana, Roti / Butter Roti, Salad, Nimbu Pani, Papad, Black Til Chutney"
        },
        "Sunday": {
            "breakfast": "Mysore Masala Dosa, Sambhar, Chutney, Veg Sandwich, Pineapple, Boiled Egg / Egg Bhurji / Paneer Bhurji",
            "lunch": "Plain Rice, Masoor Dal + Rasam, Aloo Parwal Fry, Gatte ki Sabji, Roti / Butter Roti, Curd, Salad, Chaas, Masoor Dal Chutney, Papad",
            "dinner": "Hyderabadi Veg Biriyani / Plain Rice, Arhar Dal + Sambhar, Kadhai Paneer / Chicken Lababdar / Boiled Chicken, Tandoori Roti / Plain Roti / Butter Roti, Boondi Raita, Ice Cream, Salad, Nimbu Pani, Papad, Coriander Chutney"
        },
    },
}

def parse():
    total = 0
    for hostel, weekly in MENUS.items():
        hostel_docs = []
        for day, meals in weekly.items():
            b = meals.get("breakfast", "")
            l = meals.get("lunch", "")
            d = meals.get("dinner", "")
            body = (
                f"Hostel: {hostel}. Day: {day}. Month: {MONTH}. "
                f"Breakfast (7:15 AM - 9:30 AM): {b}. "
                f"Lunch (12:00 PM - 2:00 PM): {l}. "
                f"Dinner (7:30 PM - 9:30 PM): {d}. "
                f"Daily items at breakfast: Milk, Tea/Coffee, Bread with Jam and Butter, sprouts and boiled pulses, ginger, tomato, chilli, pickle. "
                f"Daily items at lunch/dinner: Chapati (with/without ghee), Plain Rice, Jain food, Salad (Cucumber+Carrot+Tomato+Beetroot), Chilli, Onion, Lemon, fresh green chutney. "
                f"{TIMINGS}"
            )
            slug = f"{hostel.lower()}_{day.lower()}"
            filepath = f"{OUT_DIR}/mess_{slug}.txt"
            write_doc(filepath, "MESS", DATE,
                      f"{hostel} Hostel {day} Menu - August 2026", body)
            hostel_docs.append(f"{day}: Breakfast: {b[:80]}... Lunch: {l[:80]}... Dinner: {d[:80]}...")
            total += 1

        # Summary doc per hostel
        summary_body = (
            f"Mess menu for {hostel} Hostel IIT Guwahati for August 2026. "
            f"Weekly menu summary: " +
            " | ".join([f"{d}: B={MENUS[hostel][d]['breakfast'][:60]}, L={MENUS[hostel][d]['lunch'][:60]}, D={MENUS[hostel][d]['dinner'][:60]}"
                        for d in DAYS if d in MENUS[hostel]]) +
            f". {TIMINGS}"
        )
        write_doc(f"{OUT_DIR}/mess_{hostel.lower()}_summary.txt", "MESS", DATE,
                  f"{hostel} Hostel Mess Menu Summary - August 2026", summary_body)
        total += 1

    print(f"[MESS] Written {total} mess docs across {len(MENUS)} hostels")

if __name__ == "__main__":
    parse()
