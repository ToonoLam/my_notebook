/**
 * Created by Toono on 2016/12/11.
 */

var blog1 = new Vue({
    el: '#blog-comment',
    data: {
        id: location.pathname.split('/').pop(),
        comment: '',
        comments: [],
        message:''
    },
    filters: {
        marked: marked
    },
    methods: {
        submit: function() {
            var self = this;
            if (! self.comment.trim()) {
                return showAlert(self, '请输入评论内容！');
            }
            postJSON('/api/blogs/' + '001480598473277efc95dd2030242d481be8e830a1ef774000' + '/comments', {
                content: self.comment,
                time: (self.comments[0] && self.comments[0].created_at) || 0
            }, function (err, data) {
                if (err) {
                    return showAlert(self, err.message || err.data || err);
                }
                self.comment = '';
                self.comments = data.comments.concat(self.comments);
            })
        }
    },
    ready: function() {
        var self = this;
        getJSON('/api/blogs/' + '001480598473277efc95dd2030242d481be8e830a1ef774000' + '/comments', function (err, data) {
            if (err) {
                return alert(err.message || err.data || err);
                }
            self.comments = data.comments;
        });
    }
});
