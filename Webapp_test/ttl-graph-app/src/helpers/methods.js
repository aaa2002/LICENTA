const clean = (iri) => iri.split('/').pop().replace(/%20/g, ' ');

export {clean};