DEBUG = True
SECRET_KEY = 'FsdfswsskfhAOCABSKJFNAKdfbgfgaJCNWOACNQWIKXNxbcqcnskjcnIUH287R2YRHI2132FVJBKVBJSVB'
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/Users?unix_socket=/opt/lampp/var/mysql/mysql.sock'
SQLALCHEMY_TRACK_MODIFICATIONS = True  # Just to suppress warnings.

# For flask
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

# For flask debug toolbar.
DEBUG_TB_INTERCEPT_REDIRECTS = False
