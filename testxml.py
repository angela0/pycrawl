#encoding=utf-8

import lxml.html

htmldoc = u"""
<div class="C_box1">
	  <div class="box_line"></div>

		  <div class="box_txt">
	    <p class="box_title">疾病概况</p>
	    <p class="boxsearch"><a href="http://drug.health.sina.com.cn/drugStoreWare.html" class="syd">查药店</a><a href="http://hospitalize.news.sina.com/" class="sys">找医生</a></p>
	    <ul>
				<li>疾病名称：冠心病</li>
				<li>所属部位：其他</li>
				<li>就诊科室：心血管内科</li>
				<li>症状体征：（1）胸部压迫窒息感、闷胀感、剧烈的烧灼样疼痛，一般疼痛持续1-5分钟，偶有长达15分钟，可自行缓解；（2）疼痛常放射至左肩、左臂前内侧直至小指与无名指。</li>
	    </ul>
	    <dl>
	      <dt>疾病概述</dt>
	      <dd>冠状动脉性心脏病简称冠心病。指由于脂质代谢不正常，在动脉内膜一些类似粥样的脂类物质堆积而成白色斑块，称为动脉粥样硬化病变。<a href="/disease/ku/00013/bingyin.html" target="_blank">查看详细</a></dd>
	    </dl>
	    <dl>
	      <dt>临床表现</dt>
	      <dd>（1）胸部压迫窒息感、闷胀感、剧烈的烧灼样疼痛，一般疼痛持续1-5分钟，偶有长达15分钟，可自行缓解；（2）疼痛常放射至左肩、左臂前内侧直至小指与无名指。 <a href="/disease/ku/00013/zhengzhuang.html" target="_blank">查看详细</a></dd>
	    </dl>
	    <dl>
	      <dt>疾病防治</dt>
	      <dd>(1)合理饮食，不要偏食，不宜过量。要控制高胆固醇、高脂肪食物，多吃素食。同时要控制总热量的摄入，限制体重增加。 <a href="/disease/ku/00013/yufang.html" target="_blank">查看详细</a></dd>
	    </dl>
	  </div>

	  <div class="clear"></div>
	</div>
"""

doc = lxml.html.fromstring(htmldoc)

result = doc.xpath('//div[@class="box_txt"]/dl[1]/dd/text()')


print 'result'
for i in result:
    print i