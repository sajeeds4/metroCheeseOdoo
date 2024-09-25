/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class MapslyFrameView extends Component {
    setup() {
        this.rpc = useService("rpc");

        this.state = useState({
            iframeSrc: ''
        });

        onWillStart(async () => {
            const subdomain = '';

            this.state.iframeSrc = `https://${subdomain || 'app'}.mapsly.com`;
        });
    }
}

MapslyFrameView.template = "MapslyFrameView";
MapslyFrameView.display_name = "Mapsly";
MapslyFrameView.type = 'mapsly_frame_view';

// Register the component in the Owl component registry
registry.category('views').add('mapsly_frame_view', MapslyFrameView);
registry.category('actions').add('mapsly_frame_view', MapslyFrameView);
