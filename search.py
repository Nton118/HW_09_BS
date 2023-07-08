import redis
from redis_lru import RedisLRU
from db.models import Author, Quote
import db.connect


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_mongo(command, value):
    result = ""
    match command:
        case "name":
            name = value
            try:
                quotes = Quote.objects(
                    author=Author.objects.get(fullname__startswith=name)
                )
            except Exception as err:
                return err
            for quote in quotes:
                result += (quote.quote) + "\n"

        case "tag":
            tag = value
            try:
                quotes = Quote.objects(tags__startswith=tag)
            except Exception as err:
                return err
            for quote in quotes:
                result += (quote.quote) + "\n"

    return result

if __name__ == "__main__":
    print("To search, input format <command>:<value>")
    print("available commands: name, tag, tags (multiple tags comma separated), exit")
    
    while True:
        command, *value = input(">>>").split(":")
        
        if command in ("name", "tag"):
            val = str(value[0]).strip()
            print(search_mongo(command, val))
        
        elif command == "tags":
            result = ""
            tags_ = str(value[0]).strip().split(",")
            tags = [tag.strip() for tag in tags_]
            try:
                quotes = Quote.objects(tags__in=tags)
            except Exception as err:
                print(err)
            for quote in quotes:
                result += (quote.quote) + "\n"
            print(result)
            
        elif command == "exit":    
            print("good bye!")
            break
        
        else:    
            print("No such command. Try again")
