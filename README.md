# Shields.IO Visitor Counter

[![GPL-3.0](https://img.shields.io/github/license/ESKYoung/shields-io-visitor-counter?logo=GNU&logoColor=FFFFFF&style=flat-square)](https://github.com/ESKYoung/shields-io-visitor-counter/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/ESKYoung/shields-io-visitor-counter?logo=GitHub&logoColor=FFFFFF&style=flat-square)](https://github.com/ESKYoung/shields-io-visitor-counter)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?logo=Python&logoColor=FFFFFF&style=flat-square)](https://www.python.org/)Ÿ
[![Codecov](https://img.shields.io/codecov/c/github/ESKYoung/shields-io-visitor-counter/main?logo=Codecov&logoColor=FFFFFF&style=flat-square)](https://codecov.io/gh/ESKYoung/shields-io-visitor-counter)
[![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=ESKYoung.shields-io-visitor-counter&color=1D70B8&logo=GitHub&logoColor=FFFFFF&style=flat-square)](https://github.com/ESKYoung/shields-io-visitor-counter)

A simple visitor counter displayed as a Shields.IO static badge.

## How it works

This application is deployed on Heroku, and creates a Shields.IO static badge that you can embed on your page. Every
time your page loads, it reloads the badge, which pings [CountAPI][countapi] to increase the counter!

## Creating your own visitor counter

If you've used [Shields.IO][shields-io] before, it's really straightforward! Let's use the
[octocat/Spoon-Knife][spoon-knife] GitHub repository as an example.

To create a counter with all default options, add the `page` argument with your `username.repo` to the application URL:

```
https://shields-io-visitor-counter.herokuapp.com/badge?page=octocat.Spoon-Knife
```

to get this:

![Default counter](images/default_counter.svg)

And to embed this in Markdown, just use:

```
![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=octocat.Spoon-Knife)
```

### Options

The only mandatory argument is `page`, but you can use _almost_ all options available on [Shields.IO][shields-io] — the
only unavailable one is `message`, as this is the count! To add option, just add it to URL query component.

Let's take our previous example, and modify it! Say we want the following:

- Label (left-hand side) to say `My First Counter` on a black background, with a white GitHub logo;
- Message (right-hand side) to have a blue background; and
- Style it with the Shields.IO `for-the-badge` style

From the [Shields.IO][shields-io] documentation, we can:

- Change the label text using the `label` parameter;
- Change the label background colour using the `labelColor` parameter;
- Add a logo to the label, and change its colour using the `logo`, and `logoColor` parameters, respectively;
- Change the message background colour with the `color` parameter; and
- Change the badge style use the `style` parameter.

All in all, the previous URL becomes:

```
https://shields-io-visitor-counter.herokuapp.com/badge?page=octocat.Spoon-Knife&label=My First Counter&labelColor=000000&logo=GitHub&logoColor=FFFFFF&color=1D70B8&style=for-the-badge
```

which gives us:

![Custom counter](images/custom_counter.svg)

Note we used hex colours in the URL, but [Shields.IO][shields-io] also supports (some) colours by name!

## Caveats

- It's not smart enough to track users by IP address, for example. So if you reload the page, the counter will also
  increase!
- It runs on Heroku Free Tier as part of my 1,000 free dyno hours per month — if this runs out, the application will be
  down!
- Applications on Heroku Free Tier should timeout after 30 minutes, **but** I'm using [cron-job.org][cron-job] to wake
  it up every 15 minutes, so it should always be on!

If the application is down, and doesn't wake up, raise an issue, and I'll look at it as soon as possible!

## Contributing

If you'd like to contribute to this work, take a look at [`CONTRIBUTING.md`](./CONTRIBUTING.md) to get started!

## Attribution

This work is based on [Visitor Badge][visitor-badge] by Jiang Wenjian, and their excellent
[blog post][blog] on its development.

[application]: https://shields-io-visitor-counter.herokuapp.com
[blog]: https://dev.to/jwenjian/the-story-of-visitor-badge-46mm
[countapi]: https://countapi.xyz/
[cron-job]: https://cron-job.org/
[shields-io]: https://shields.io/
[spoon-knife]: https://github.com/octocat/Spoon-Knife
[visitor-badge]: https://github.com/jwenjian/visitor-badge
