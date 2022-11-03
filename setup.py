from setuptools import setup

setup(
    name='azurefastapi',
    version='0.1.0',    
    description='A wrapper to run FastAPI in Azure Containers',
    url='https://github.com/SharmaAjay19/AzureFastAPI',
    author='Ajay Sharma',
    author_email='ajsharm@microsoft.com',
    license='BSD 2-clause',
    packages=['azurefastapi'],
    install_requires=['fastapi',
                      'uvicorn',
                      'redis',
                      'azure-cosmos',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)