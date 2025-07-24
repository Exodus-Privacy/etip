# Useful commands

Some admin commands are available to help administrate the ETIP database.

## Compare with Exodus

This command retrieves trackers data from an εxodus instance and looks for differences with trackers in the local database.

```sh
python manage.py compare_with_exodus
```

Note: for now, it only compares with local trackers having the flag `is_in_exodus`.

The default εxodus instance queried is the public one available at <https://reports.exodus-privacy.eu.org> (see `--exodus-hostname` parameter).

