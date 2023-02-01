from siamese import inference

class find:
    def similar(id):
        person = []
        who = inference.run("static/login/" + id + ".png")
        person.append(who)
        return person