(function() {
    function setTextOrValue(ctrls, val) {
        /**
         * Set text or value appropriately for each control.
         */
        ctrls.each(function(i, el) {
            el = $(el);
            if (el.is('input'))
                el.val(val);
            else
                el.text(val);
        });
    }

    function addForwardingAddress(addr) {
        var input = $('<input type="email" />');
        input.addClass('form-control');
        input.attr('placeholder', 'john@gmail.com');
        if (addr)
            input.val(addr);
        var emailCol = $('<div />');
        emailCol.addClass('col-xs-11 forward-to-input-col');
        emailCol.append(input);

        var removeButton = $('<button type="button" />');
        removeButton.addClass('btn btn-small btn-block btn-default');
        removeButton.attr('disabled', 'disabled');
        var removeIcon = $('<span />');
        removeIcon.attr('aria-hidden', 'true');
        removeIcon.addClass('glyphicon glyphicon-minus');
        removeButton.append(removeIcon);
        removeButton.on('click', function() {
            if (row.attr('data-hiding') !== 'true') {
                row.attr('data-hiding', 'true').stop(true).slideUp(200, function() {
                    row.remove();
                });
                updateDisabledButtons(this);
            }
        }.bind(this));
        var removeCol = $('<div />');
        removeCol.addClass('forward-to-remove-col col-xs-1');
        removeCol.append(removeButton);

        var row = $('<div class="row" />');
        row.hide();
        row.append(emailCol);
        row.append(removeCol);
        this.append(row);
        row.slideDown(200);

        updateDisabledButtons(this);
    }

    function updateDisabledButtons(ctrl) {
        if (ctrl.find('.row[data-hiding!="true"]').length > 1)
            ctrl.find('button').attr('disabled', false);
        else
            ctrl.find('button').attr('disabled', 'disabled');
    }

    function updateForwardToValue() {
        var modal = $(this);
        var addrs = [];
        modal.find('.js-forward-to-addresses input').each(function(i, el) {
            el = $(el);
            addrs.push(el.val());
        });
        modal.find('.js-forward-to').val(addrs.join(','));
    }

    function updateForwardToAddr() {
        var modal = $(this);
        var name = modal.find('input[name=name]').val();
        var domain = modal.data('domain');

        if (name.indexOf('@') !== -1) {
            modal.find('.js-warn-addr').show();
            modal.find('button').attr('disabled', 'disabled');
        } else {
            modal.find('.js-addr').val(name + '@' + domain);
            modal.find('.js-warn-addr').hide();
            modal.find('button').attr('disabled', false);
        }
    }

    function showAddAddressModal(domain, isWildcard) {
        var modal = $('#js-modal-add-address');
        modal.data('domain', domain);
        setTextOrValue(modal.find('.js-domain'), domain);

        if (isWildcard) {
            modal.addClass('js-wildcard');
        } else {
            modal.removeClass('js-wildcard');
        }

        modal.find('input[name=password],input[name=name]').val('');
        modal.find('button').attr('disabled', false);
        modal.find('input[name=name]').off('input').on('input', updateForwardToAddr.bind(modal));

        var container = modal.find('.js-forward-to-addresses');
        var addAddress = addForwardingAddress.bind(container);
        container.empty();
        addAddress();

        modal.find('.js-add-another').off('click').on('click', function() { addAddress(); });
        modal.parent('form').off('submit').on('submit', function() {
            updateForwardToValue.bind(this)();
            updateForwardToAddr.bind(this)();
        }.bind(modal));
        modal.modal();
    }

    $(document).ready(function() {
        $('.js-change-password').on('click', function() {
            var modal = $('#js-modal-change-password');
            setTextOrValue(modal.find('.js-email'), $(this).data('addr'));
            modal.find('input[name=password]').val('');
            modal.modal();
        });

        $('.js-remove-address').on('click', function() {
            var modal = $('#js-modal-remove-address');
            setTextOrValue(modal.find('.js-email'), $(this).data('addr'));
            modal.modal();
        });

        $('.js-add-address').on('click', function() {
            showAddAddressModal($(this).data('domain'), false);
        });

        $('.js-edit-forward-to').on('click', function() {
            var modal = $('#js-modal-edit-forward-to');
            setTextOrValue(modal.find('.js-email'), $(this).data('addr'));

            var container = modal.find('.js-forward-to-addresses');
            var addAddress = addForwardingAddress.bind(container);
            container.empty();

            var forwardTo = $(this).data('forward-to').split(',');
            for (var i = 0; i < forwardTo.length; i++)
                addAddress(forwardTo[i]);

            modal.find('.js-add-another').on('click', function() { addAddress(); });
            modal.find('button[type=submit]').on('click', updateForwardToValue.bind(modal));

            modal.modal();
        });

        var catchallTitle = '<strong>Catch-all forwarding addresses</strong>';
        var catchallContent = ' \
            <p>A catch-all address is used when a message arrives that doesn\'t match any other forwarding rule.</p> \
            <p>You\'re not required to have one, but you can use one if you\'d like.</p> \
        ';


        $('.js-catchall-whats-this').popover({
            'title': catchallTitle,
            'content': catchallContent,
            'html': true
        }).on('click', function() {
            $(this).popover('toggle');
        });

        $('.js-add-catchall').popover({
            'title': catchallTitle,
            'content': catchallContent + ' \
                <a class="btn btn-large btn-block btn-success js-add-catchall-btn">Add a catch-all address</a> \
            ',
            'html': true
        }).on('click', function() {
            $(this).popover('toggle');
            $('.js-add-catchall-btn').on('click', function() {
                $(this).popover('hide');
                showAddAddressModal($(this).data('domain'), true);
            }.bind(this));
        });

        $('.js-import-csv').on('change', function() {
            $('.js-import-csv-form').trigger('submit');
        });
    });
})();

// vim: ts=4 sts=4 sw=4
