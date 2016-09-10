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
        removeButton.click(function() {
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
            ctrl.find('button').removeAttr('disabled');
        else
            ctrl.find('button').attr('disabled', 'disabled');
    }

    function updateForwardToValue() {
        var addrs = [];
        // TODO: use _.pluck or something
        this.find('.js-forward-to-addresses input').each(function(i, el) {
            el = $(el);
            addrs.push(el.val());
        });
        this.find('.js-forward-to').val(addrs.join(','));
    }

    $(document).ready(function() {
        $('.js-change-password').click(function() {
            var modal = $('#js-modal-change-password');
            setTextOrValue(modal.find('.js-email'), $(this).data('addr'));
            modal.find('input[name=password]').val('');
            modal.modal();
        });

        $('.js-remove-address').click(function() {
            var modal = $('#js-modal-remove-address');
            setTextOrValue(modal.find('.js-email'), $(this).data('addr'));
            modal.modal();
        });

        $('.js-add-address').click(function() {
            var modal = $('#js-modal-add-address');
            var domain = $(this).data('domain');
            setTextOrValue(modal.find('.js-domain'), domain);
            modal.find('input[name=password],input[name=name]').val('');
            modal.find('button').removeAttr('disabled');
            modal.find('input[name=name]').on('input', function() {
                if ($(this).val().indexOf('@') !== -1) {
                    modal.find('.js-warn-addr').show();
                    modal.find('button').attr('disabled', 'disabled');
                } else {
                    modal.find('.js-addr').val($(this).val() + '@' + domain);
                    modal.find('.js-warn-addr').hide();
                    modal.find('button').removeAttr('disabled');
                }
            });

            var container = modal.find('.js-forward-to-addresses');
            var addAddress = addForwardingAddress.bind(container);
            container.empty();
            addAddress();

            modal.find('.js-add-another').click(function() { addAddress(); });
            // TODO: what if they submit another way
            modal.find('button[type=submit]').click(updateForwardToValue.bind(modal));
            modal.modal();
        });

        $('.js-edit-forward-to').click(function() {
            var modal = $('#js-modal-edit-forward-to');
            setTextOrValue(modal.find('.js-email'), $(this).data('addr'));

            var container = modal.find('.js-forward-to-addresses');
            var addAddress = addForwardingAddress.bind(container);
            container.empty();

            var forwardTo = $(this).data('forward-to').split(',');
            for (var i = 0; i < forwardTo.length; i++)
                addAddress(forwardTo[i]);

            modal.find('.js-add-another').click(function() { addAddress(); });
            modal.find('button[type=submit]').click(updateForwardToValue.bind(modal));

            modal.modal();
        });
    });
})();
