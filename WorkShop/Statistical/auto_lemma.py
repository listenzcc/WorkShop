# File: auto_lemma.py
# Aim: Automatically parse the .tex files in current folder,
#      find all lemmas and generate sub .tex files for them

import os

# ! Use __file__'s folder by default
folder = os.path.dirname(__file__)


def tex_files(folder=folder):
    return [os.path.join(folder, n)
            for n in os.listdir(folder)
            if n.endswith('.tex')]


class Lemma_in_LaTeX(object):
    # * Find Lemmas in LaTeX file,
    # * auto generate LaTeX file for them
    def __init__(self, path):
        # path is the path of the .tex file,
        # generate raw content in self.raw
        assert(path.endswith('.tex'))
        self.raw = open(path).read()
        self.path = path

    def fetch_lemmas(self):
        # Fetch all lemmas in the raw content,
        # legal lemmas should starts with head and ends with tail
        print('------------------------------------------------------')
        print(f'Fetching Lemmas in {self.path}')
        head = '\\begin{lemma}'
        tail = '\\end{lemma}'
        lemmas = [e.split(tail)[0].strip()
                  for e in self.raw.split(head)
                  if tail in e]

        # Make lemma_table as [lemma_key]: [lemma_contents]
        lemma_table = dict()
        for lemma in lemmas:
            label, contents = self.parse_lemma(lemma)
            assert(len(label.strip()) > 0)
            assert(len(contents.strip()) > 0)
            assert(label not in lemma_table)
            lemma_table[label] = contents
        # print(lemma_table)

        # Generate LaTeX files for lemmas
        folder = os.path.join(os.path.dirname(self.path), 'lemmas')
        if not os.path.isdir(folder):
            os.mkdir(folder)

        subfiles = '{subfiles}'
        tex = os.path.basename(self.path)
        document_class = f'\documentclass[../{tex}]{subfiles}\n'

        suggestions = []

        for name in lemma_table:
            _name = name.strip()
            path = os.path.join(folder, f'{_name}.tex').encode()

            suggestions.append('\\subfile{lemmas/' + _name + '}')

            if os.path.isfile(path):
                print(f'Warning: Lemma file of {name} exists.')
                # continue

            with open(path, 'wb') as f:
                # * Add documentclass
                f.write(document_class.encode())
                f.write(b'\n')

                # * Start document
                f.write(b'\\begin{document}\n')

                # * Add ref
                f.write(b'\\subsubsection{Explain of Lemma\\ref{Lemma:')
                f.write(name.encode())
                f.write(b'}}\n')

                # * Add content as raw LaTeX
                __name = '{' + _name + '}'
                f.write(f'\\textbf{__name}\n'.encode())
                f.write(b'% ---------------------------------------\n')
                f.write(b'%    Original contents\n')
                f.write(
                    f'%    File: ..\\{os.path.basename(self.path)}\n'.encode())
                f.write(b'\\begin{quote}\n')
                content = lemma_table[name].encode()
                f.write(content)
                f.write(b'\n')
                f.write(b'\\end{quote}\n')
                f.write(b'% ---------------------------------------\n\n')

                # * White paper
                f.write(b'% ---------------------------------------\n')
                f.write(b'%    Your word goes here\n\n')
                f.write(b'% ---------------------------------------\n')

                # * End document
                f.write(b'\\end{document}\n')

                print(f'Logging: Lemma file of {name} is generated.')

        print(f'\nSuggestions of {self.path} is:')
        print('\n'.join(suggestions))
        print()

    def parse_lemma(self, lemma):
        # Get label and content of the lemma
        head = '\\label{Lemma:'
        splitter = '\n'
        lines = lemma.split(splitter)
        label = [e for e in lines if e.startswith(head)][0][len(head):-1]
        contents = [e for e in lines if not e.startswith(head)]
        return label, splitter.join(contents)


if __name__ == '__main__':
    for path in tex_files():
        lil = Lemma_in_LaTeX(path)
        lil.fetch_lemmas()
