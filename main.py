from chains.master_chain import master_chain


if __name__ == "__main__":
    while True:
        uid = input("User ID: ")
        msg = input("Message: ")


        output = master_chain.invoke({
        "user_id": uid,
        "input": msg,
        })
        print("AI:", output)