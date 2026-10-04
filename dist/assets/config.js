// Preview defaults. Never enable an endpoint without approved privacy practices.
// An endpoint must validate server-side, rate-limit, reject spam and return
// { received: true } only after the enquiry is durably received.
window.AASHRAY_CONFIG = Object.freeze({ enquiryEndpoint: null, formsApproved: false });
