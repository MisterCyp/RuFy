jQuery.fn.dataTableExt.type.order['file-size-pre'] = function ( data ) {
    var matches = data.match( /^(\d+(?:\.\d+)?)\s*([a-z]+)/i );
    var multipliers = {
        o: 1,
        ko: 1000,
        kio: 1024,
        mo: 1000000,
        mio: 1048576,
        go: 1000000000,
        gio: 1073741824,
        to: 1000000000000,
        tio: 1099511627776,
        po: 1000000000000000,
        pio: 1125899906842624
    };
                                                                                                                                                                      
    if (matches) {
        var multiplier = multipliers[matches[2].toLowerCase()];
        return parseFloat( matches[1] ) * multiplier;
    } else {
        return -1;
    };
};
jQuery.fn.dataTableExt.type.order['date-pub-pre'] = function ( data ) {
    var matches = data.match( /^(\d+(?:\.\d+)?)\s*([a-z]+)/i );
    var multipliers = {
	heure: 1,
        heures: 1,
	jour: 24,
        jours: 24,
        mois: 720,
	an: 8640,
        ans: 8640
    };
                                                                                                                                                                      
    if (matches) {
        var multiplier = multipliers[matches[2].toLowerCase()];
        return parseFloat( matches[1] ) * multiplier;
    } else {
        return -1;
    };
};
