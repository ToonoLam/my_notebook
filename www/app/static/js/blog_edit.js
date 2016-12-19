
var vm = new Vue({
    el: '#blog',
    data: {
        action: '/api/blogs',
        message: '',
        blog: {
            name: '',
            summary: '',
            content: ''
        },
    },
    filters: {
        marked: marked
    },
    ready: function () {
        if (location.pathname.split('/').pop() === 'edit') {
            var id = getUrlParams('id');
            this.action = this.action + '/' + id;
            getJSON(this.action, function (err, blog) {
                vm.blog = blog;
            });
        }
    },
    methods: {
        click: function (folder) {
            this.blog.summary  = folder;
        },
        submit: function () {
            postJSON(this.action, this.blog, function (err, blog) {
                if (err) {
                    return showAlert(vm, err.message || err.data || err)
                }
                return location.assign(location.pathname.split('bootstrap')[0] + 'blog/' + blog.id);
            });
        }
    }
});

