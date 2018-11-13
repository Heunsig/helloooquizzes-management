class CaTemplate {
  constructor (template, data) {
    this.template = template
    this.data = data
  }


  extract () {
    var re = /(<%(\w+)?%>|&lt;%(\w+)?%&gt;)/g
    var match = null
    var tbl = this.template
    while(match = re.exec(this.template)) {
      let key = match[2] ? match[2] : match[3]
      tbl = tbl.replace(match[0], this.data[key])
    }

    return tbl
  }


  render () {
    return this.extract()
  }
}