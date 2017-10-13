odoo.define("vz_subscription_planning.GridRenderer", function (require) {
    "use strict";
    var GridRenderer = require("web_grid.GridRenderer");
    var GridView = require("web_grid.GridView");
    var GridModel = require('web_grid.GridModel');
    var GridController = require('web_grid.GridController');

    GridRenderer.include({

        _isCellReadonly: function (cell) {
            var _this = this;
            var date = new Date()
            var date_limit = new Date();
            date_limit.setDate(date_limit.getDate() + 2);

            if(_this.state.context.params.model != 'sale.subscription.planning.line') return this._super.apply(this, arguments);

            var res = !this.editableCells || cell.readonly;
            var res2 = true;
            for (var i = 0; i < cell.domain.length; i++) {
                if (cell.domain[i].constructor === Array) {
                    if (cell.domain[i][0] === 'date' && cell.domain[i][1] === '>=')
                    {
                        date = new Date(cell.domain[i][2]);
                        if (date < date_limit) res2 = res2 && true;
                        else res2 = res2 && false;
                    }
                }
            }
            return res || res2;
        },

    });


});
