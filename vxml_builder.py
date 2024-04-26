import xml.etree.ElementTree as ET
import inflect

class Home:
    home_path = "test.xml"

    def __init__(self) -> None:
        with open(self.home_path, 'r') as file:
            self.vxml_template = file.read()

        ET.register_namespace("", "http://www.w3.org/2001/vxml")
        self.p = inflect.engine()

    def reload(self):
        with open(self.home_path, 'r') as file:
            self.vxml_template = file.read()

    def add_menu_option(self, tree, dtmf, prompt_text, next_url):
        menu = tree.find('{http://www.w3.org/2001/vxml}menu')
        
        prompt = menu.find('{http://www.w3.org/2001/vxml}prompt')
        prompt.text += f"If you want to know the results of the question: \"{prompt_text}\", Please press or say {dtmf}."

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
                question_start = prompt.text.find(f"Please press or say {dtmf}")
                if question_start != -1:
                    question_end = prompt.text.find("Please press or say", question_start + 1)
                    prompt.text = prompt.text[:question_start] + (prompt.text[question_end:] if question_end != -1 else "")
                break

        root = tree.getroot()
        self.vxml_template = ET.tostring(root, encoding='unicode', method='xml')
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
        last = max([ int(choice.get("dtmf")) for choice in choices ], default=0)

        for option in options:
            last += 1
            self.add_menu_option(tree, last, option['prompt'], option['url'])
        
        root = tree.getroot()
        self.vxml_template = ET.tostring(root, encoding='unicode', method='xml')
        return self.vxml_template 

    def delete(self, dtmf):
        self.delete_menu_option(dtmf)
        self.reorder()

    def commit(self):
        with open(self.home_path, 'w') as file:
            self.vxml_template = file.write(self.vxml_template)

options = [
    {'prompt': 'do you think trees on farmland are better than clearing the land before sowing?', 'url': 'http://webhosting.voxeo.net/209394/www/question1.xml'},
    {'prompt': 'Is it better to preserve historical buildings or replace them with modern infrastructure?', 'url': 'http://webhosting.voxeo.net/209394/www/question2.xml'},
    {'prompt': 'Is it more effective to manage forest fires through prevention techniques rather than suppression methods after they start?', 'url': 'http://webhosting.voxeo.net/209394/www/question3.xml'}
]

vxml = Home()
# updated_vxml = vxml.delete_menu_option(9)
updated_vxml = vxml.updated_vxml(options)
vxml.delete(8)
updated_vxml = vxml.updated_vxml(options)
print(updated_vxml)
vxml.commit()
