This is the repo for [http://xun-wei.com](http://xun-wei.com).

Access info of Database, AWS keys, and other relevant stuff should be kept in `secret.py`, which is ignored in `git`.

To start:

    $ mkvirtualenv xunwei-website
    $ pip install -r requirements.txt
    $ npm install

To dev:

    $ npm start
    $ python manage.py runserver

To build front-end:

    $ npm run-script build
    $ python manage.py collectstatic --noinput