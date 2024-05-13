import xml.etree.ElementTree as ET
import inflect


class PhoneBuilder:
    def __init__(self, number, domain):
        self.template = f"""
        <vxml xmlns="http://www.w3.org/2001/vxml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0" xsi:schemaLocation="http://www.w3.org/2001/vxml              http://www.w3.org/TR/voicexml20/vxml.xsd">
            <form>
                <block>
                    <submit next="{domain}api/vote/{number}" method="get"/>
                </block>
            </form>
            <prompt>
                Voted!
            </prompt>
            <catch event="error">
                <prompt>There was an error processing your request.</prompt>
            </catch>

            <disconnect/>
        </vxml>
        """
        self.number = number

    def commit(self):
        with open("./vxml/" + self.number + ".xml", "w") as f:
            f.write(self.template)


class QuestionBuilder:
    def __init__(self, yes: int, no: int, domain: str, uuid: str):
        self.template = f"""<?xml version="1.0" encoding="ISO-8859-1"?>
        <vxml version="2.0" xmlns="http://www.w3.org/2001/vxml"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.w3.org/2001/vxml
        http://www.w3.org/TR/voicexml20/vxml.xsd">
        <menu>
        <property name="inputmodes" value="dtmf voice"/>
        <prompt>
            The number of votes for "yes" on this question is {yes}, and for "no" is {no}. To view results for other questions, press or say 1.
        </prompt>
        <choice dtmf="1" accept="exact" next="{domain}vxml/root.xml">
            One
        </choice>
        <noinput>Please say or press one <enumerate/></noinput>
        </menu>
        </vxml>
        """
        self.uuid = uuid

    def commit(self):
        with open("./vxml/" + self.uuid + ".xml", "w") as f:
            f.write(self.template)


class HomeBuilder:
    home_path = "vxml/root.xml"

    def __init__(self) -> None:
        with open(self.home_path, 'r') as file:
            self.vxml_template = file.read()

        ET.register_namespace("", "http://www.w3.org/2001/vxml")
        self.p = inflect.engine()

    def reload(self):
        with open(self.home_path, 'r') as file:
            self.vxml_template = file.read()

    def add_menu_option(self, tree, dtmf, prompt_text, next_url, audio_url):
        menu = tree.find('{http://www.w3.org/2001/vxml}menu')

        prompt = menu.find('{http://www.w3.org/2001/vxml}prompt')
        prompt.text += f"If you want to know the results of the question: \"{prompt_text}\", Please press or say {dtmf}."

        audio_fr = ET.Element("audio")
        audio_fr.set("src", audio_url + "-french.mp3")

        audio_sp = ET.Element("audio")
        audio_sp.set("src", audio_url + "-bambara.mp3")

        audio_it = ET.Element("audio")
        audio_it.set("src", audio_url + "-fula.mp3")

        audio_bo = ET.Element("audio")
        audio_bo.set("src", audio_url + "-bobo.mp3")

        prompt.append(audio_fr)
        prompt.append(audio_sp)
        prompt.append(audio_it)
        prompt.append(audio_bo)

        choice = ET.Element('choice')
        choice.set('dtmf', str(dtmf))
        choice.set('accept', 'exact')
        choice.set('next', next_url)
        dtmf = self.p.number_to_words(dtmf)
        choice.text = str(dtmf)

        menu.append(choice)

    def delete_menu_option(self, dtmf):
        tree = ET.ElementTree(ET.fromstring(self.vxml_template))
        menu = tree.find('{http://www.w3.org/2001/vxml}menu')

        prompt = menu.find('{http://www.w3.org/2001/vxml}prompt')
        choices = list(menu.findall('{http://www.w3.org/2001/vxml}choice'))
        for choice in choices:
            if choice.get('dtmf') == str(dtmf):
                # Remove the choice
                menu.remove(choice)
                # Update the prompt text to remove the related text
                question_start = prompt.text.find(
                    f"Please press or say {dtmf}")
                if question_start != -1:
                    question_end = prompt.text.find(
                        "Please press or say", question_start + 1)
                    prompt.text = prompt.text[:question_start] + (
                        prompt.text[question_end:] if question_end != -1 else "")
                break

        root = tree.getroot()
        self.vxml_template = ET.tostring(
            root, encoding='unicode', method='xml')
        return self.vxml_template

    def remove_all(self):
        tree = ET.ElementTree(ET.fromstring(self.vxml_template))
        menu = tree.find('{http://www.w3.org/2001/vxml}menu')
        choices = menu.findall('{http://www.w3.org/2001/vxml}choice')

        # Remove all
        for choice in choices:
            dtmf = int(choice.get('dtmf'))
            self.delete_menu_option(dtmf)

    def reorder(self):
        tree = ET.ElementTree(ET.fromstring(self.vxml_template))
        menu = tree.find('{http://www.w3.org/2001/vxml}menu')
        prompt_text = menu.find('{http://www.w3.org/2001/vxml}prompt').text
        # Extract questions
        import re
        questions = re.findall(r'\"(.*?)\"', prompt_text)

        options = []
        choices = menu.findall('{http://www.w3.org/2001/vxml}choice')

        self.remove_all()
        for i, choice in enumerate(choices):
            dtmf = i + 1
            url = choice.get('next')
            option = {'dtmf': dtmf, 'prompt': questions[i], 'url': url}
            options.append(option)

        self.updated_vxml(options)

        return self.vxml_template

    def updated_vxml(self, options):
        tree = ET.ElementTree(ET.fromstring(self.vxml_template))
        menu = tree.find('{http://www.w3.org/2001/vxml}menu')
        choices = menu.findall('{http://www.w3.org/2001/vxml}choice')

        # Get the end dtmf.
        last = max([int(choice.get("dtmf")) for choice in choices], default=0)

        for option in options:
            last += 1
            self.add_menu_option(
                tree,
                last,
                option['prompt'],
                option['url'],
                option["audio_url"])

        root = tree.getroot()
        self.vxml_template = ET.tostring(
            root, encoding='unicode', method='xml')
        return self.vxml_template

    def delete(self, dtmf):
        self.delete_menu_option(dtmf)
        self.reorder()

    def commit(self):
        with open(self.home_path, 'w') as file:
            self.vxml_template = file.write(self.vxml_template)
