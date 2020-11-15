import os


def get_environment():
    return (os.environ.get('ENVIRONMENT') or os.environ['OPENSHIFT_BUILD_NAMESPACE'].split('-')[-1]).upper()


if __name__ == '__main__':
    print(get_environment())
