# Evidence and contact rules

## Source hierarchy

Prefer sources in this order:

1. official company website and official documents;
2. government registry, tax authority, customs authority, or exchange filing;
3. official LinkedIn or other official company social page;
4. industry association, chamber, authorized dealer directory, or supplier's official distributor page;
5. Google Business or established local business directory;
6. commercial company/contact database as supporting evidence only.

Search-result snippets can locate evidence but should not be the sole basis for a final claim when the underlying page is accessible.

## Identity closure

Accept a source only when the target company is closed by at least two meaningful signals, such as:

- exact or legally equivalent company name;
- correct country and city;
- matching address or tax/company number;
- official domain referenced by a government, association, supplier, or official social profile;
- matching phone, email domain, brand relationship, or product range.

Name similarity alone is insufficient. Watch for common names, different-country branches, platform-owned contact details, generic website-builder profiles, and search substring collisions.

## Website review

Inspect the homepage plus relevant Product, Service, Contact, About, Team, Management, Procurement, Dealer, Rental, and Branch pages. When text extraction is sparse or misleading, inspect the rendered page and specific product images/captions. Generic stock images do not prove industry relevance.

Record:

- `Website Status`: Verified, Unverified, Invalid/Inactive, or No Website Found;
- the exact page URLs used;
- a short business summary based on observed content;
- whether the conclusion is fact or `推测`.

## Email rules

- Never synthesize an email from a name and domain.
- Prefer procurement and decision contacts; retain general corporate email when no better address exists.
- Avoid HR, recruiting, accounting, IT, press, marketing, privacy, abuse, and support mailboxes unless the task specifically targets them or no other contact exists and the user wants maximum coverage.
- Treat third-party database emails as Medium/Low confidence unless corroborated.
- Store every rejected or non-Good address only in working audit data, not in the user-facing Zoho Email field.

## Phone and WhatsApp

- Prefer `tel:` links and numbers in identified company contact sections.
- Reject dates, coordinates, registration numbers, SKU/model numbers, analytics IDs, and directory/platform contact numbers.
- A mobile number is not automatically WhatsApp.
- Set `WhatsApp` only for an explicit WhatsApp label, WhatsApp button, `wa.me` link, or `api.whatsapp.com/send` link tied to the company.
- Normalize country code and digits while preserving the displayed source value in audit data when useful.

## Social and directory fallbacks

Official Facebook, LinkedIn, Instagram, and X pages can establish company identity and publish contacts. Independently found profiles require name, country/address, domain, or phone closure.

Yellow pages, chambers, associations, government directories, and supplier dealer lists are valuable when the company has no website. They do not justify copying the platform's own email or phone to the target company.

## False-positive handling

When an automated result is wrong:

- record `Rejected Identity URL` and a concise rejection reason;
- do not reuse its website, email, phone, or social profiles;
- keep the customs company if product evidence remains credible;
- set manual review when the correct public identity remains unresolved.
