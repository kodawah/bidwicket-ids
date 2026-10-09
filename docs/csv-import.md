# CSV import notes

The [BidWicket integration guide](http://bidwicket.com/Help/Custom_Site_Integration.html)
describes seller access to Store → Store Connect → Ccg Single Codes. Those
sheets remain an authoritative way to obtain codes when available.
For the measured profiles, this encoder can build full IDs locally instead.

A tested buylist import has this shape; replace the store label as needed:

```csv
#Usc Id,Inventory Name,Store Name,Buy #,Buy $,Sell #,Sell $
USCIDU-637-F-06911-287-TES-EFM,x,Your Store,1,0,NC,0
```

The identifier and `Buy #` quantity are the relevant tested fields. The
example's generic store label was not itself part of the recorded live test.

Observed on profile 637:

- Two three-row uploads accepted six previously unexported IDs, including
  requested quantities of one, two, and three. Maximum batch size is unknown.
- A malformed ID stopped processing later rows in controlled tests. Earlier
  valid rows were accepted. Validate the entire input before uploading.
- `Buy #` supplied the quantity sold to the store; the resulting buylist
  export recorded the quantity in `Sell #`. Blind round-tripping is unsafe.
- Some exported card names contained unquoted commas, producing malformed
  CSV fields. The original readback verification took the ID from the first
  field and quantity from the second-to-last field.
- Empty anonymous carts did not process the tested Tools import request.
  A normal add followed by one bulk import worked; a flow with no seed add
  remains unverified.
- The Update form changed existing rows only. Repeated `Buy` query parameters
  added only the last product in the tested request.

This repository generates identifiers only. Cart initialization, browser
handoff, quantity limits, and larger batches need integration testing.
