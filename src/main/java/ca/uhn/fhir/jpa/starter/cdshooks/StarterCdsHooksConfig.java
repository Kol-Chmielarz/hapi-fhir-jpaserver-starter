package ca.uhn.fhir.jpa.starter.cdshooks;

import org.hl7.fhir.instance.model.api.IBaseResource;
import org.springframework.beans.factory.FactoryBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.AutowireCapableBeanFactory;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

import ca.uhn.fhir.jpa.cache.IResourceChangeListenerRegistry;
import ca.uhn.fhir.rest.server.RestfulServer;
import ca.uhn.hapi.fhir.cdshooks.api.ICdsHooksDaoAuthorizationSvc;
import ca.uhn.hapi.fhir.cdshooks.config.CdsHooksConfig;
import ca.uhn.hapi.fhir.cdshooks.svc.CdsHooksContextBooter;

@Configuration
@Import(CdsHooksConfig.class)
public class StarterCdsHooksConfig {
	@Bean
	public CdsHooksContextBooter cdsHooksContextBooter() {
		// ourLog.info("No Spring Context provided.  Assuming all CDS Services will be registered dynamically.");
		return new CdsHooksContextBooter();
	}

	public static class CdsHooksDaoAuthorizationSvc implements ICdsHooksDaoAuthorizationSvc {
		@Override
		public void authorizePreShow(IBaseResource theResource) {}
	}

	@Bean
	ICdsHooksDaoAuthorizationSvc cdsHooksDaoAuthorizationSvc() {
		return new CdsHooksDaoAuthorizationSvc();
	}

	@Bean
	public ServletRegistrationBean<CdsHooksServlet> cdsHooksRegistrationBean(AutowireCapableBeanFactory beanFactory) {
		CdsHooksServlet cdsHooksServlet = new CdsHooksServlet();
		beanFactory.autowireBean(cdsHooksServlet);

		ServletRegistrationBean<CdsHooksServlet> registrationBean = new ServletRegistrationBean<>();
		registrationBean.setName("cds-hooks servlet");
		registrationBean.setServlet(cdsHooksServlet);
		registrationBean.addUrlMappings("/cds-services/*");
		registrationBean.setLoadOnStartup(1);
		return registrationBean;
	}
}