[[!meta title="economode: turn economode on/off on the printers"]]

By default our printers print with the Economode setting on, which saves toner
and also means your printouts come out draft quality. If you need to print
something and not have it in draft quality, you can use the `economode` script
to turn Economode off.

You'll need the printer password, whose location can be found in the
[[private docs|doc staff/private]].

Remember to reset Economode to on using the same script once you're done.

## Usage

```text
$ economode on
Enter printer password:
Setting economode to on for papercut... OK
Setting economode to on for pagefault... OK

$ economode off
Enter printer password:
Setting economode to off for papercut... OK
Setting economode to off for pagefault... OK
```
