const InstrumentRow = Vue.component('instrument-row', {
    props: [
        'instrument',
        'instrumentprofileurl',
        'instrumentediturl',
    ],
    delimiters: ['[[',']]'],
    template: `
        <tr class="item-row">
            <th scope="row" class="inventory-number">[[ instrument.inventory_number ]]</th>
            <td scope="row" class="name">[[ instrument.name ]]</td>
            <td class="text-center">
                <i :class="['fa', instrument.is_active ? 'fa-check text-success' : 'fa-times text-danger', 'td-active']" :active="instrument.is_active"></i>
            </td>
            <td scope="row" class="text-center">
                <div class="dropdown">
                    <button type="button" class="white-button btn-sm dropdown-toggle" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="fa fa-cog"></i>
                    </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" :href="instrumentprofileurl"></i> Ver detalle</a>
                        <a class="dropdown-item" :href="instrumentediturl"><i class="fa fa-edit"></i> Modificar datos</a>
                        <button type="submit" @click="switchInstrumentStatus(instrument.id)" class="dropdown-item">
                            <span v-if="instrument.is_active"><i class="fa fa-ban"></i> Deshabilitar</span>
                            <span v-else><i class="fa fa-check"></i> Habilitar</span>
                        </button>
                    </div>
                </div>
            </td>
        </tr>
    `,
    methods: {
        switchInstrumentStatus(instrumentId) {
            fetch('/api/instrumentos/' + instrumentId + '/estado', {
                method: 'PATCH'
            })
                .then(response => {
                    return response.json()
                })
                .then(json => {
                    console.log(json);
                    this.$emit('statuschanged', json.status, this.instrument);
                })
        },
    }
});

export {InstrumentRow};