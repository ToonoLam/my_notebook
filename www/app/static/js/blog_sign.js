/**
 * Created by Toono on 2016/12/8.
 */
var vmSignIn = new Vue({
    el: '#vm-sign-in',
    data: {
        email: '',
        password: '',
        message: ''
    },
    methods: {
        submit: function(){
            var self = this;
            self.signin_email = self.signin_email.trim();
            if(! self.signin_email ){
                return showAlert(self, '请输入email');
            }
            postJSON('/blog/signin', {
                email: self.signin_email,
                sha1_pw: self.password==='' ? '' : CryptoJS.SHA1(self.signin_email + ':' + self.password).toString()
            }, function(err, result){
                if (err) {
                    return showAlert(self, err.message || err.data || err);
                }
                return location.assign(location.pathname.split('signin')[0]);
            });
        }
    }
});


function validateEmail(email) {
  var re = /^[\w\.\-]+\@[\w\-]+(\.[\w\-]+){1,4}$/;
  return re.test(email);
}

var vmSignUp = new Vue({
    el: '#vm-sign-up',
    data: {
        name: getUrlParams('name') || '',
        email: '',
        password1: '',
        password2: '',
        message:'',
    },
    methods: {
        submit: function(){
            var self = this;
            self.name = self.name.trim();
            self.signup_email = self.signup_email.trim();

            if (! self.name) {
                return showAlert(self, '请输入名字');
            }
            if (! validateEmail(self.signup_email)) {
                return showAlert(self, '请输入正确的Email地址');
            }
            if (self.password1.length < 6) {
                return showAlert(self, '口令长度至少为6个字符');
            }
            if (self.password1 !== self.password2) {
                return showAlert(self, '两次输入的口令不一致');
            }
            
            postJSON('/blog/signup', {
                name: self.name,
                email: self.signup_email,
                sha1_pw: CryptoJS.SHA1(self.signup_email + ':' + self.password1).toString(),
                oid: getUrlParams('oid'),
                image: getUrlParams('image')
            }, function (err, result) {
                if (err) {
                    return showAlert(self, err.message || err.data || err);
                }
                return location.assign(location.pathname.split('signup')[0]);
            });
        }
    }
});