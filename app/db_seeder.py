import asyncio
from app.database import async_session_maker, init_db
from app.models import Word, Grammar

# Words data
WORDS = [
    {"vietnamese_word": "chào", "english_definition": "hello/goodbye"},
    {"vietnamese_word": "cô", "english_definition": "I/you (woman of older generation)"},
    {"vietnamese_word": "em", "english_definition": "I/you (younger person or informal)"},
    {"vietnamese_word": "tên", "english_definition": "name"},
    {"vietnamese_word": "gì", "english_definition": "what"},
    {"vietnamese_word": "hả", "english_definition": "huh? (expression of surprise or clarification)"},
    {"vietnamese_word": "dạ", "english_definition": "yes (polite/formal) or politeness marker when responding"},
    {"vietnamese_word": "cũng", "english_definition": "also/too"},
    {"vietnamese_word": "hay", "english_definition": "interesting/cool"},
    {"vietnamese_word": "vì", "english_definition": "because"},
    {"vietnamese_word": "không", "english_definition": "no/not"},
    {"vietnamese_word": "chị", "english_definition": "I/you (older sister or woman of similar age)"},
    {"vietnamese_word": "anh", "english_definition": "I/you (older brother or man of similar age)"},
    {"vietnamese_word": "là", "english_definition": "am/are/is (to be)"},
    {"vietnamese_word": "người", "english_definition": "person"},
    {"vietnamese_word": "nước", "english_definition": "country or water"},
    {"vietnamese_word": "nào", "english_definition": "which"},
    {"vietnamese_word": "tiếng", "english_definition": "language/speech"},
    {"vietnamese_word": "mọi người", "english_definition": "everyone"},
    {"vietnamese_word": "tại sao", "english_definition": "why"},
    {"vietnamese_word": "học", "english_definition": "study/learn"},
    {"vietnamese_word": "ủa", "english_definition": "huh? (surprised exclamation)"},
    {"vietnamese_word": "đây", "english_definition": "this/here (near speaker)"},
    {"vietnamese_word": "lớp", "english_definition": "class"},
    {"vietnamese_word": "làm", "english_definition": "do/make"},
    {"vietnamese_word": "nhân viên", "english_definition": "employee/office worker"},
    {"vietnamese_word": "văn phòng", "english_definition": "office"},
    {"vietnamese_word": "giáo viên", "english_definition": "teacher"},
    {"vietnamese_word": "thiệt", "english_definition": "really/truly (Southern dialect)"},
    {"vietnamese_word": "của", "english_definition": "of/belonging to (possessive marker)"},
    {"vietnamese_word": "sống", "english_definition": "live (to be alive or reside)"},
    {"vietnamese_word": "ở", "english_definition": "at/in/live (location or residence)"},
    {"vietnamese_word": "đi", "english_definition": "go"},
    {"vietnamese_word": "chưa", "english_definition": "not yet"},
    {"vietnamese_word": "còn", "english_definition": "still/remaining"},
    {"vietnamese_word": "bao nhiêu", "english_definition": "how much/how many"},
    {"vietnamese_word": "tuổi", "english_definition": "age"},
    {"vietnamese_word": "chồng", "english_definition": "husband"},
    {"vietnamese_word": "vợ", "english_definition": "wife"},
    {"vietnamese_word": "bạn", "english_definition": "friend"},
    {"vietnamese_word": "bạn trai", "english_definition": "boyfriend"},
    {"vietnamese_word": "bạn gái", "english_definition": "girlfriend"},
    {"vietnamese_word": "có", "english_definition": "have/yes"},
    {"vietnamese_word": "bàn", "english_definition": "table"},
    {"vietnamese_word": "ghế", "english_definition": "chair"},
    {"vietnamese_word": "điện thoại", "english_definition": "mobile phone"},
    {"vietnamese_word": "ba lô", "english_definition": "backpack"},
    {"vietnamese_word": "ly", "english_definition": "glass (for drinking)"},
    {"vietnamese_word": "ai", "english_definition": "who"},
    {"vietnamese_word": "quá", "english_definition": "very/too (indicates extreme degree)"},
    {"vietnamese_word": "giỏi", "english_definition": "good/well/talented"},
    {"vietnamese_word": "nói", "english_definition": "speak/say"},
    {"vietnamese_word": "dở", "english_definition": "bad/badly"},
    {"vietnamese_word": "biết", "english_definition": "know"},
    {"vietnamese_word": "một", "english_definition": "one (number 1)"},
    {"vietnamese_word": "hai", "english_definition": "two (number 2)"},
    {"vietnamese_word": "ba", "english_definition": "three (number 3) or father"},
    {"vietnamese_word": "bốn", "english_definition": "four (number 4)"},
    {"vietnamese_word": "năm", "english_definition": "five (number 5)"},
    {"vietnamese_word": "sáu", "english_definition": "six (number 6)"},
    {"vietnamese_word": "bảy", "english_definition": "seven (number 7)"},
    {"vietnamese_word": "tám", "english_definition": "eight (number 8)"},
    {"vietnamese_word": "chín", "english_definition": "nine (number 9)"},
    {"vietnamese_word": "mười", "english_definition": "ten (number 10)"},
    {"vietnamese_word": "một trăm", "english_definition": "one hundred (100)"},
    {"vietnamese_word": "một ngàn", "english_definition": "one thousand (1000)"},
    {"vietnamese_word": "mười ngàn", "english_definition": "ten thousand (10000)"},
    {"vietnamese_word": "vậy", "english_definition": "so/thus"},
    {"vietnamese_word": "phải", "english_definition": "right/correct/must"},
    {"vietnamese_word": "mẹ", "english_definition": "mother"},
    {"vietnamese_word": "ba mẹ", "english_definition": "parents"},
    {"vietnamese_word": "xe máy", "english_definition": "motorbike"},
    {"vietnamese_word": "để", "english_definition": "let/in order to"},
    {"vietnamese_word": "chở", "english_definition": "give a ride to/carry (on vehicle)"},
    {"vietnamese_word": "đẹp", "english_definition": "beautiful/pretty"},
    {"vietnamese_word": "ơi", "english_definition": "hey (vocative particle to get attention)"},
    {"vietnamese_word": "ngày mai", "english_definition": "tomorrow"},
    {"vietnamese_word": "ăn", "english_definition": "eat"},
    {"vietnamese_word": "ăn tối", "english_definition": "have dinner/eat dinner"},
    {"vietnamese_word": "thích", "english_definition": "like"},
    {"vietnamese_word": "uống", "english_definition": "drink"},
    {"vietnamese_word": "đồ ăn", "english_definition": "food"},
    {"vietnamese_word": "phở", "english_definition": "pho (Vietnamese noodle soup)"},
    {"vietnamese_word": "chả giò", "english_definition": "spring rolls"},
    {"vietnamese_word": "cơm", "english_definition": "rice (cooked)"},
    {"vietnamese_word": "bánh mì", "english_definition": "bread/Vietnamese sandwich"},
    {"vietnamese_word": "cà phê sữa đá", "english_definition": "iced coffee with milk"},
    {"vietnamese_word": "trà", "english_definition": "tea"},
    {"vietnamese_word": "bia", "english_definition": "beer"},
    {"vietnamese_word": "con", "english_definition": "I/you (person of younger generation, used by/to children)"},
    {"vietnamese_word": "cho", "english_definition": "give/for"},
    {"vietnamese_word": "muốn", "english_definition": "want"},
    {"vietnamese_word": "cơm tấm", "english_definition": "broken rice (Vietnamese dish)"},
    {"vietnamese_word": "rồi", "english_definition": "already/got it/OK"},
    {"vietnamese_word": "ngon", "english_definition": "delicious/tasty"}
]

# Grammar data
GRAMMAR = [
    {
        "grammar_point": "Không sao",
        "english_explanation": "Expression meaning 'no problem' or 'it's okay'",
        "example_sentence": "Không sao đâu! (No problem!)"
    },
    {
        "grammar_point": "Còn...?",
        "english_explanation": "Follow-up question particle meaning 'and...?' or 'what about...?'",
        "example_sentence": "Em là người Việt. Còn anh? (I'm Vietnamese. And you?)"
    },
    {
        "grammar_point": "Ở đâu",
        "english_explanation": "Question word for location meaning 'where'",
        "example_sentence": "Nhà vệ sinh ở đâu? (Where is the bathroom?)"
    },
    {
        "grammar_point": "Cũng vậy",
        "english_explanation": "Expression meaning 'me too' or 'same here'",
        "example_sentence": "Em thích phở. – Cũng vậy! (I like pho. – Me too!)"
    },
    {
        "grammar_point": "Ở đây",
        "english_explanation": "Expression meaning 'here' (location)",
        "example_sentence": "Em đang ở đây. (I am here now.)"
    },
    {
        "grammar_point": "Không có",
        "english_explanation": "Negative form meaning 'not have' or 'don't have'",
        "example_sentence": "Em không có tiền. (I don't have money.)"
    },
    {
        "grammar_point": "Chưa có",
        "english_explanation": "Negative form meaning 'not yet have' or 'don't have yet'",
        "example_sentence": "Em chưa có con. (I don't have children yet.)"
    },
    {
        "grammar_point": "Cái đó",
        "english_explanation": "Demonstrative meaning 'that thing'",
        "example_sentence": "Cái đó là điện thoại của em. (That is my phone.)"
    },
    {
        "grammar_point": "Cái này",
        "english_explanation": "Demonstrative meaning 'this thing'",
        "example_sentence": "Cái này là gì? (What is this?)"
    },
    {
        "grammar_point": "Cái gì",
        "english_explanation": "Question word for things meaning 'what thing' or 'what'",
        "example_sentence": "Em đang làm cái gì? (What are you doing?)"
    },
    {
        "grammar_point": "Của ai",
        "english_explanation": "Possessive question meaning 'whose'",
        "example_sentence": "Đây là sách của ai? (Whose book is this?)"
    },
    {
        "grammar_point": "Thiệt hả?",
        "english_explanation": "Question phrase meaning 'Really?' (Southern Vietnamese)",
        "example_sentence": "Em làm hết rồi. – Thiệt hả? (I finished everything. – Really?)"
    },
    {
        "grammar_point": "phải không",
        "english_explanation": "Tag question meaning 'right?' added to end of statements for confirmation",
        "example_sentence": "Em là người Mỹ, phải không? (You're American, right?)"
    },
    {
        "grammar_point": "không phải là",
        "english_explanation": "Negative form of 'to be' meaning 'am not/are not/is not'",
        "example_sentence": "Em không phải là người Mỹ. (I'm not American.)"
    },
    {
        "grammar_point": "... nữa",
        "english_explanation": "Particle meaning 'as well' or 'also', placed after the item being included",
        "example_sentence": "Em thích cà phê nữa. (I like coffee as well.)"
    },
    {
        "grammar_point": "Cho con...",
        "english_explanation": "Request pattern meaning 'Give me...' (when child/younger person asks elder)",
        "example_sentence": "Cho con một ly nước. (Give me a glass of water.)"
    },
    {
        "grammar_point": "... này",
        "english_explanation": "Demonstrative modifier meaning 'this' placed after the noun",
        "example_sentence": "Cái bàn này mới. (This table is new.)"
    },
    {
        "grammar_point": "Em thích ăn gì?",
        "english_explanation": "Question pattern: 'What do you like to eat?' - structure is [subject] + thích + [verb] + gì",
        "example_sentence": "Em thích ăn gì? (What do you like to eat?)"
    },
    {
        "grammar_point": "Em thích ăn...",
        "english_explanation": "Statement pattern: 'I like to eat...' - structure is [subject] + thích + [verb] + [object]",
        "example_sentence": "Em thích ăn phở. (I like to eat pho.)"
    },
    {
        "grammar_point": "Em không thích ăn...",
        "english_explanation": "Negative statement pattern: 'I don't like to eat...' - use không before thích to negate",
        "example_sentence": "Em không thích ăn cơm. (I don't like to eat rice.)"
    },
    {
        "grammar_point": "Em muốn ăn gì?",
        "english_explanation": "Question pattern: 'What do you want to eat?' - structure is [subject] + muốn + [verb] + gì",
        "example_sentence": "Em muốn ăn gì? (What do you want to eat?)"
    },
    {
        "grammar_point": "Em muốn ăn...",
        "english_explanation": "Statement pattern: 'I want to eat...' - structure is [subject] + muốn + [verb] + [object]",
        "example_sentence": "Em muốn ăn bánh mì. (I want to eat bread.)"
    },
    {
        "grammar_point": "Ngon quá!",
        "english_explanation": "Exclamation pattern using 'quá' after adjective to express 'so/very/too' with emphasis",
        "example_sentence": "Ngon quá! (So delicious!)"
    }
]


async def seed_database() -> None:
    """Seed the database with initial words and grammar."""
    print("Initializing database...")
    await init_db()
    
    async with async_session_maker() as session:
        print(f"Adding {len(WORDS)} words...")
        for word_data in WORDS:
            word = Word(**word_data)
            session.add(word)
        
        print(f"Adding {len(GRAMMAR)} grammar points...")
        for grammar_data in GRAMMAR:
            grammar = Grammar(**grammar_data)
            session.add(grammar)
        
        await session.commit()
        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())