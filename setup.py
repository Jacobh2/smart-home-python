from setuptools import setup

install_requires = [
    "google-api-python-client",
    "requests"
]

setup(
    name="smart_home_python",
    version="0.1.1",
    description="Smart Home Python Google Action Library",
    url="https://github.com/Jacobh2/smart-home-python",
    install_requires=install_requires,
    author="Jacob Hagstedt",
    author_email="jacob.hagstedt@gmail.com",
    license="MIT",
    packages=["smart_home"],
    zip_safe=False,
)
