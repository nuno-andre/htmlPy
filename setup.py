from distutils.core import setup

setup(
    name='htmlPy',
    version='1.6.0',
    author='Amol Mandhane',
    author_email='amol.mandhane@gmail.com',
    packages=['htmlPy'],
    scripts=[],
    url='http://pypi.python.org/pypi/htmlPy/',
    license='LICENSE.txt',
    description="A wrapper around PyQt4's webkit library which helps developer create beautiful UI with HTML5, CSS and Javascript for standalone applications.",
    long_description=open('README.txt').read(),
    install_requires=["Jinja2>=2.6"],
    dependency_links = [
        "http://www.riverbankcomputing.com/software/pyqt/download"
    ],
)
