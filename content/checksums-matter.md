Title: Checksums matter
Date: 2023-06-30
Category: Programming
Tags: best-practices
Summary: When serving files over the internet, TCP and SSL are not enough.

When dealing with user uploaded files or static assets in your project it is a
common practice to store the file in a CDN or the filesystem and an entry that
references it on a database.

When serving those files, you send a url to the user to fetch the file.

Now you may think that just by using a token or https that will be enough to
download the right file from the server, after all, the ssl handshake will
ensure you connect to the right server, the url was built and served in a
trusted environment and the TCP protocol will take care of ensuring the transfer
succeeds and gracefully handle any network errors/disconnects.

The problem is that all those checks are important but missing one key point:
You can correctly and securely get the wrong file. TCP and SSL are not enough.

Since the data is stored in a separate location or service, that service could
be compromised and the files could be tempered. Not only that, the service could
be temporally unavailable and instead of downloading the file you expected, your
client downloaded an HTML error page.

A checksum is a hash of the file that can be served along the URI of the file so
that the client can verify that the downloaded file is indeed the one intended
to be downloaded from that URI.

As a bonus, no extra checks are needed from the client, since this will take
care of problems with the file size, file format, etc. The checksums need to
match, period.

[1]: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity "Subresource Integrity"
