## Web4 (Web, 200pts)

> Bruteforce the JWT secret to become admin
> 
> [http://139.59.69.138:17723](http://139.59.69.138:17723)

![](start.jpg)

The site sets this cookie `auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjpudWxsfQ.pgMKdpUKL8fYGe79FRUR2mBLCsJRGI1DjVDwrRs_9mo`, which obviously is a [JWT](https://jwt.io/introduction/).

The `Setec astronomy` is a reference to the [Sneakers (1992 film)](https://en.wikipedia.org/wiki/Sneakers_(1992_film)) in which `Setec Astronomy` is an anagram of `Too many secrets`.

![](https://gph.is/18xMFzP)

Using the debugger at [jwt.io](https://jwt.io/#debugger) we confirm that `Too many secrets` is the secret used to create the JWT. Knowing the secret we can edit the payload of the token, so we set the user to `admin`.

![](jwt.jpg)

Setting the new JWT as the cookie value we are logged in as `admin`.

![](solution.jpg)
