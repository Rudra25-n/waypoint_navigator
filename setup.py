from setuptools import find_packages, setup

package_name = 'waypoint_navigator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rudra Bhosale',
    maintainer_email='warlord@todo.todo',
    description='Sequential Nav2 waypoint navigation for TurtleBot3',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
             'waypoint_navigator = waypoint_navigator.navigator:main',
        ],
    },
)




