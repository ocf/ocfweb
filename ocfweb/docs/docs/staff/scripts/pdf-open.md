[[!meta title="pdf-open: unf*&^ bad PDFs if they won't print right"]]

## Introduction

The `pdf-open` script is used when lab users attempt to print PDFs that our
printers don't like for myriad reasons. The easiest solution is to rasterize
the PDF and send it for printing again, hoping the printer gods are merciful.
Examples of PDFs that commonly fail include many Econ 136 and Bio 1B papers,
PDFs with strange images or scanned components in them, and things people try
to print straight from Gmail attachment viewer.

If a user comes asking why their paper isn't printing right, first download the
PDF, then run `pdf-open $pdf_file`. Don't forget the hyphen, and make sure the
filename doesn't have any spaces or weird characters in it. After
re-rasterizing the file, Evince will open, and you can start a new print job
from there. Monitor the job's progress in
[printhost.ocf.berkeley.edu](//printhost.ocf.berkeley.edu) to ensure the job
survives. You may [[refund|doc staff/scripts/paper]] printing credits to
the user in case they've gone over their daily capacity and you're feeling
generous.
